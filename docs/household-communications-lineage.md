# Household Communications Lineage

Observed and reframed on 2026-08-14.

## Decision

Treat Nagz, Famster, and SharedSpaceLab as one product lineage with different roles:

| Component | Role | Lifecycle |
|---|---|---|
| SharedSpaceLab | Current successor experiment and product-discovery surface | Active prototype |
| ConversationLab | Reusable conversation kernel | Active package |
| CoordinationLab | Reusable coordination kernel | Active package |
| Nagz iOS | Working legacy implementation and behavior reference | Legacy reference |
| Famster iOS | Thin concept shell created during the family-product split | Concept only |
| 1041Kit | Generic client infrastructure that Famster does not currently initialize | Candidate package |
| Nagzerver | Mixed production infrastructure with several non-Nagz consumers | Live; separately governed |

This reframing does not rename the future product or assign it to BillDonner.com or
1041soft.com. Those remain owner decisions.

## What The Source Shows

### Nagz

Nagz is a substantial working family reminder and communication system. Its iOS source contains
implemented family membership, connections, reminder flows, and more than 215 tests. The iOS,
web, AI, and server repositories form a real prior implementation, although substantive product
work slowed after April 2026.

Use Nagz as a behavior catalog and compatibility reference. New household-facing features should
not default to the Nagz app.

### Famster

Famster is not an independent working product. Its current app has seven Swift source files;
Home, Family, and Calendar are placeholders, and 1041Kit setup is commented out. The only network
activity is a warm-up request to `https://api.famster.app/version`.

`api.famster.app` resolves to the same Nagzerver deployment. It is not a separate Famster
backend. `/api/v1/version` identifies the Nagz API, while Famster's `/version` request receives
the static Nagz web fallback.

Do not continue Famster as a parallel app. Preserve its name, ASC history, and sketches until the
successor's public identity is decided.

### SharedSpaceLab

SharedSpaceLab is the active successor experiment. It already brings together commitments,
roles, schedules, family broadcasts, two-person lifecycles, and multi-person rehearsals in a
friendlier household interface. It has adaptive iPhone and iPad UI, nearby peer chat through
Multipeer Connectivity, 52 tests, a local MCP server and harness, and Mac Catalyst support.

Its lack of server, account, Nagz, or Famster integration is deliberate. Wall-mounted iPads are
the current test proxy for anticipated shared touchscreen home devices.

## Infrastructure Boundary

Nagzerver is no longer just the Nagz server. The live service currently exposes:

| Surface | Live API paths | Consumers |
|---|---:|---|
| PickledBalls v2-style API | 37 `/api/v1/pb/*` | PickledBalls |
| PickleFamilia legacy API | 14 `/api/v1/pickle/*` | PickleFamilia |
| workin On | 7 `/api/v1/workinon/*` | workin On, including APNs |
| Clubwatch transport | 4 routes | Residual LtWatcher compatibility only |
| Nagz family API | Remaining API | Nagz clients and web surfaces |

Therefore, product retirement and server retirement are separate decisions. Nagzerver can only be
split or retired route family by route family after each consumer has moved.

The exact source running in Fly release v100 was absent from Git `main`. It is preserved at
private branch `recovery/deployed-2026-06-30`, commit `a57211b`. That source generates all 163
live API paths. Its test suite reports 1,113 passed and one failure:
`tests/test_pickleball_sessions.py::test_player_schedule`.

Do not redeploy from main or merge the recovery branch wholesale until that difference is reviewed.

## Migration Sequence

1. Continue SharedSpaceLab as a local-first household interaction prototype.
2. Keep ConversationLab and CoordinationLab small and reusable; extract only behavior already
   exercised by SharedSpaceLab.
3. Inventory Nagz capabilities by user outcome, not by existing screen or endpoint.
4. Port a Nagz capability only after SharedSpaceLab demonstrates a need that local or nearby-peer
   behavior cannot satisfy.
5. When remote identity, off-LAN messaging, durable group state, or APNs becomes necessary, define
   a clean household API contract before reusing Nagzerver internals.
6. Keep Famster paused. Reuse its name only if it wins the later naming decision.
7. Reconcile the deployed Nagzerver recovery branch, fix the PickledBalls schedule defect, and
   separate route ownership before considering backend retirement.

## Open Decisions

- Public product name: SharedSpaceLab, Famster, Nagz, or a new name.
- Product line: permanently free BillDonner.com or commercial-grade 1041soft.com.
- Distribution: private household experiment, TestFlight product, or supported release.
- Native Mac requirement versus Mac Catalyst as an internal testing surface.
- Server boundary and privacy model once off-LAN communication is justified.
- Whether the eventual target includes only Apple household surfaces or broader clients.
