# Ctrlable Control4

A Home Assistant / **Ctrlable Pro** integration for **Control4** systems. Connects
to a local Control4 Director over its REST + WebSocket APIs and brings Control4
devices into Ctrlable Pro with real-time (push) updates.

Supports lights, switches, blinds/covers, fans, thermostats/climate, media
players/rooms, locks, sensors, binary sensors, and security panels — plus
**full Control4 keypad support** (button events + LED control) when paired with
the companion [Ctrlable Control4 keypad driver](https://github.com/Ctrlable/ctrlable-c4-drivers).

## Features

- **Local push** — real-time updates over the Director WebSocket, no polling.
- **Selective device import** — choose exactly which Control4 devices to bring
  into Ctrlable Pro. A domain filter (by Control4 proxy type) plus a
  type-to-search device picker means large systems don't flood Home Assistant
  with every item. Defaults to importing everything for a first-run experience.
- **Keypad events + LEDs** — physical Control4 keypad presses surface as
  `ctrlable_control4_keypad_event` events, and keypad button LEDs can be driven
  from Ctrlable Pro in real time (via the companion keypad driver).
- **Licensed** — activated with a key issued by
  [portal.ctrlable.com](https://portal.ctrlable.com).

## Installation

Install via the **Ctrlable Store** / HACS, then add the integration:

1. Settings → Devices & Services → **Add Integration** → *Ctrlable Control4*.
2. Enter the controller IP, your Control4 account username/password, and your
   Ctrlable Control4 **license key**.
3. In the integration's **Configure** dialog, either keep *Import every Control4
   device* or uncheck it to pick specific devices (with a domain filter and
   search).

## Keypads

For reliable keypad button events and LED control across all keypad models,
install the **Ctrlable Control4 Keypad** DriverWorks driver from
[`ctrlable-c4-drivers`](https://github.com/Ctrlable/ctrlable-c4-drivers) onto the
controller and bind it to the Ctrlable Coordinator. The driver forwards presses
to this integration and mirrors LED state back to the physical keypad.

## Attribution

Derived from the Apache-2.0 licensed `hass-control4` and `pyControl4` projects.
See [`NOTICE`](NOTICE) and [`LICENSE`](LICENSE).
