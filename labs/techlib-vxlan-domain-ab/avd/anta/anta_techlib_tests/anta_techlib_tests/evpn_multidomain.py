"""Custom ANTA tests — EVPN multi-domain (techlib-vxlan-domain-ab).

Three tests the stock library cannot express:

* VerifyEVPNType4Routes  — ES (Type-4) route presence. With `identifier
  auto lacp` there is no static ES-Import RT, so seeing the PEER's Type-4
  route proves the af-evpn `route type ethernet-segment route-target auto`
  machinery is importing (the Day 54 s6 functional patch).
* VerifyEVPNDFElection   — designated-forwarder expectation per interface.
* VerifyEVPNDPath        — D-PATH domain identifiers on routes that crossed
  the domain boundary.

MOCK-VERIFIED: the parsing targets the documented shapes below; the first
live run may require shape adjustment (flagged inline where EOS JSON is
reconstructed from operational experience rather than captured output).
"""
from __future__ import annotations

from anta.models import AntaCommand, AntaTemplate, AntaTest


class VerifyEVPNType4Routes(AntaTest):
    """Expect at least `minimum` EVPN Type-4 (Ethernet Segment) routes.

    For a two-member all-active ES, `minimum: 2` proves the peer's ES route
    was IMPORTED (the local route is always present) — i.e. auto ES-Import
    RT derivation is working end to end.
    """

    categories = ["evpn", "multihoming"]
    commands = [AntaCommand(command="show bgp evpn route-type ethernet-segment", revision=2)]

    class Input(AntaTest.Input):
        minimum: int = 2
        esis: list[str] = []
        """Optional ESI substrings that must each appear in at least one route key."""

    @AntaTest.anta_test
    def test(self) -> None:
        out = self.instance_commands[0].json_output
        routes = out.get("vrfs", {}).get("default", {}).get("evpnRoutes", {})
        count = len(routes)
        if count < self.inputs.minimum:
            self.result.is_failure(f"Type-4 routes: {count} < minimum {self.inputs.minimum} — peer ES route not imported (check es-rt-auto)")
            return
        missing = [e for e in self.inputs.esis if not any(e in k for k in routes)]
        if missing:
            self.result.is_failure(f"Type-4 routes missing expected ESI(s): {missing}")
            return
        self.result.is_success()


class VerifyEVPNDFElection(AntaTest):
    """Assert this device's DF verdict for one ES-bearing interface.

    Parses the TEXT output of `show bgp evpn instance` (documented in the
    Arista VXLAN Configuration guide): each instance block lists
    `Local IP address:` and, under `Local ethernet segment:`, the ESI,
    `Interface:`, and `Designated forwarder: <VTEP IP>`. The device is the
    DF when the designated-forwarder IP equals the instance's local IP.
    DF election is per-ES/EVI — with the preference algorithm the verdict
    must be uniform across instances; any split is reported.
    """

    categories = ["evpn", "multihoming"]
    commands = [AntaCommand(command="show bgp evpn instance", ofmt="text")]

    class Input(AntaTest.Input):
        interface: str
        expect_df: bool

    @AntaTest.anta_test
    def test(self) -> None:
        text = self.instance_commands[0].text_output
        local_ip: str | None = None
        in_target = False
        verdicts: list[bool] = []
        for raw in text.splitlines():
            line = raw.strip()
            if line.startswith("Local IP address:"):
                local_ip = line.split(":", 1)[1].strip()
            elif line.startswith("Interface:"):
                in_target = line.split(":", 1)[1].strip() == self.inputs.interface
            elif line.startswith("Designated forwarder:") and in_target:
                verdicts.append(line.split(":", 1)[1].strip() == local_ip)
                in_target = False
        if not verdicts:
            self.result.is_failure(f"No Ethernet Segment on {self.inputs.interface} in any EVPN instance")
            return
        if all(v is self.inputs.expect_df for v in verdicts):
            self.result.is_success()
            return
        self.result.is_failure(
            f"{self.inputs.interface}: expected designated_forwarder={self.inputs.expect_df}, "
            f"observed DF in {sum(verdicts)}/{len(verdicts)} instance(s)"
        )


class VerifyEVPNDPath(AntaTest):
    """Assert D-PATH domain identifiers on a boundary-crossing prefix.

    SHAPE NOTE: parses `show bgp evpn route-type ip-prefix {prefix} detail`;
    expects path entries carrying `dPath.domains[].id` (reconstructed shape).
    """

    categories = ["evpn", "gateway"]

    class Input(AntaTest.Input):
        prefix: str
        expected_domains: list[str]

    @staticmethod
    def _templates() -> list[AntaTemplate]:
        return [AntaTemplate(template="show bgp evpn route-type ip-prefix {prefix} detail", revision=2)]

    commands = _templates()

    def render(self, template: AntaTemplate) -> list[AntaCommand]:
        return [template.render(prefix=self.inputs.prefix)]

    @AntaTest.anta_test
    def test(self) -> None:
        out = self.instance_commands[0].json_output
        routes = out.get("vrfs", {}).get("default", {}).get("evpnRoutes", {})
        seen: set[str] = set()
        for r in routes.values():
            for p in r.get("evpnRoutePaths", []):
                for d in p.get("dPath", {}).get("domains", []):
                    if "id" in d:
                        seen.add(d["id"])
        missing = [d for d in self.inputs.expected_domains if d not in seen]
        if missing:
            self.result.is_failure(f"{self.inputs.prefix}: D-PATH missing domain id(s) {missing}; saw {sorted(seen)}")
            return
        self.result.is_success()
