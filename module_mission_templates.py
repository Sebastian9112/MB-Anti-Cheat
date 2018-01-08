#MBAC begin
mb_anti_cheat = [
  (ti_server_player_joined, 0, 0, [],
  [
    (call_script, "script_mbac_ti_player_joined"),
  ]),

  (ti_on_multiplayer_mission_end, 0, 0, [],
  [
    (call_script, "script_mbac_ti_mission_end"),
  ]),

  (ti_on_agent_spawn, 0, 0, [],
  [
    (call_script, "script_cf_mbac_ti_agent_spawn"),
  ]),

  (ti_on_agent_hit, 0, 0, [],
  [
    (call_script, "script_cf_mbac_ti_agent_hit"),
  ]),

  (0, 0, ti_once, [],
  [
    (call_script, "script_mbac_ti_once"),
  ]),
  
  (0, 0, 0, [],
  [
    (call_script, "script_mbac_ti_each_frame"),
  ]),
]
#MBAC end
