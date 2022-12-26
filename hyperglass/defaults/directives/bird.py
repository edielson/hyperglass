"""Default BIRD Directives."""

# Project
from hyperglass.models.directive import Rule, Text, BuiltinDirective

__all__ = (
    "BIRD_BGPASPath",
    "BIRD_BGPCommunity",
    "BIRD_BGPRoute",
    "BIRD_Ping",
    "BIRD_Traceroute",
)

BIRD_BGPRoute = BuiltinDirective(
    id="__hyperglass_bird_bgp_route__",
    name="BGP Route",
    rules=[
        Rule(
            condition="0.0.0.0/0",
            action="permit",
            command='birdc "show route all where {target} ~ net"',
        ),
        Rule(
            condition="::/0",
            action="permit",
            command='birdc "show route all where {target} ~ net"',
        ),
    ],
    field=Text(description="IP Address, Prefix, or Hostname"),
    platforms=["bird"],
)

BIRD_BGPASPath = BuiltinDirective(
    id="__hyperglass_bird_bgp_aspath__",
    name="BGP AS Path",
    rules=[
        Rule(
            condition="*",
            action="permit",
            commands=[
                'birdc "show route all where bgp_path ~ {target}"',
            ],
        )
    ],
    field=Text(description="AS Path Regular Expression"),
    platforms=["bird"],
)

BIRD_BGPCommunity = BuiltinDirective(
    id="__hyperglass_bird_bgp_community__",
    name="BGP Community",
    rules=[
        Rule(
            condition="*",
            action="permit",
            commands=[
                'birdc "show route all where {target} ~ bgp_community"',
            ],
        )
    ],
    field=Text(description="BGP Community String"),
    platforms=["bird"],
)

BIRD_Ping = BuiltinDirective(
    id="__hyperglass_bird_ping__",
    name="Ping",
    rules=[
        Rule(
            condition="0.0.0.0/0",
            action="permit",
            command="ping -4 -c 5 -I {source4} {target}",
        ),
        Rule(
            condition="::/0",
            action="permit",
            command="ping -6 -c 5 -I {source6} {target}",
        ),
    ],
    field=Text(description="IP Address, Prefix, or Hostname"),
    platforms=["bird"],
)

BIRD_Traceroute = BuiltinDirective(
    id="__hyperglass_bird_traceroute__",
    name="Traceroute",
    rules=[
        Rule(
            condition="0.0.0.0/0",
            action="permit",
            command="traceroute -4 -w 1 -q 1 -s {source4} {target}",
        ),
        Rule(
            condition="::/0",
            action="permit",
            command="traceroute -6 -w 1 -q 1 -s {source6} {target}",
        ),
    ],
    field=Text(description="IP Address, Prefix, or Hostname"),
    platforms=["bird"],
)
