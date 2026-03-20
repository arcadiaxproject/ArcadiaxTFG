"""
Test manual de la ArcadeStateMachine.
Prueba todas las transiciones validas e invalidas.

Uso:
    cd arcade
    python test_state_machine.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from arcade.playback.state_machine import ArcadeStateMachine, State


def test(desc, resultado, esperado):
    ok = resultado == esperado
    estado = "OK" if ok else "ERROR"
    print(f"  [{estado}] {desc} -> {resultado} (esperado: {esperado})")
    if not ok:
        sys.exit(1)


print("\n=== TEST ArcadeStateMachine ===\n")

# ── Transiciones VALIDAS ─────────────────────────────────

print("--- Transiciones validas ---")

sm = ArcadeStateMachine()
test("IDLE -> TRAILER",    sm.transition(State.TRAILER),   True)
test("Estado es TRAILER",  sm.state,                       State.TRAILER)

test("TRAILER -> SELECTING", sm.transition(State.SELECTING), True)
test("SELECTING -> LOADING", sm.transition(State.LOADING),   True)
test("LOADING -> PLAYING",   sm.transition(State.PLAYING),   True)
test("PLAYING -> SAVING",    sm.transition(State.SAVING),    True)
test("SAVING -> PLAYING",    sm.transition(State.PLAYING),   True)
test("PLAYING -> IDLE",      sm.transition(State.IDLE),      True)

# ── Transiciones INVALIDAS ───────────────────────────────

print("\n--- Transiciones invalidas (deben devolver False) ---")

sm = ArcadeStateMachine()  # IDLE
test("IDLE -> PLAYING (invalido)",   sm.transition(State.PLAYING), False)
test("IDLE -> SAVING (invalido)",    sm.transition(State.SAVING),  False)
test("IDLE -> LOADING (invalido)",   sm.transition(State.LOADING), False)
test("Estado sigue siendo IDLE",     sm.state,                     State.IDLE)

sm.transition(State.SELECTING)  # IDLE -> SELECTING
test("SELECTING -> TRAILER (invalido)", sm.transition(State.TRAILER), False)
test("SELECTING -> PLAYING (invalido)", sm.transition(State.PLAYING), False)

# ── Propiedades ──────────────────────────────────────────

print("\n--- Propiedades is_idle / is_selecting / is_playing ---")

sm = ArcadeStateMachine()
test("IDLE: is_idle=True",      sm.is_idle,      True)
test("IDLE: is_playing=False",  sm.is_playing,   False)

sm.transition(State.SELECTING)
test("SELECTING: is_selecting=True", sm.is_selecting, True)

sm.transition(State.LOADING)
sm.transition(State.PLAYING)
test("PLAYING: is_playing=True",  sm.is_playing, True)

sm.transition(State.SAVING)
test("SAVING: is_playing=True (sigue jugando)", sm.is_playing, True)

print("\n=== TODOS LOS TESTS PASADOS ===\n")
