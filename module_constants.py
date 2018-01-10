#MBAC begin
mbac_v_maj = 0
mbac_v_min = 8
mbac_v_rev = 5

msg_log_only = -1
msg_players = 0
msg_admins = 1

hack_unblockable = 0
hack_autoblock = 1
hack_aimbot = 2
num_hacks = 3

con_message = -1
con_perma_ban = 0
con_temp_ban = 1
con_kick = 2

hack_detection = []#set default hack detection, 0 or 1
hack_detection.append(1)#unblockable
hack_detection.append(1)#autoblock
hack_detection.append(1)#aimbot

hack_percentage = []
hack_percentage.append(13)#percentage of ignored blocks to trigger a warning
hack_percentage.append(75)#percentage of down blocks to trigger a warning
hack_percentage.append(75)#percentage of head shots to trigger a warning

hack_consequence = []#set default consequence per hack
hack_consequence.append(con_temp_ban)#unblockable
hack_consequence.append(con_message)#autoblock
hack_consequence.append(con_message)#aimbot

hack_warn_threshold = []#set default number of hack incidents to trigger a warning
hack_warn_threshold.append(2)#unblockable
hack_warn_threshold.append(4)#autoblock
hack_warn_threshold.append(3)#aimbot

cmd_advanced_logging = 0
cmd_player_join_message = 1
cmd_broadcast_hack_warnings = 2
cmd_broadcast_hack_consequences = 3
cmd_hacks_option = 4
cmd_hacks_consequence = cmd_hacks_option + num_hacks
cmd_end = cmd_hacks_consequence + num_hacks

slot_troop_enable_anti_cheat = 1000
slot_troop_hack_percentage = 1001
slot_troop_hack_consequence = 1002
slot_troop_hack_warn_threshold = 1003
slot_troop_item_attack_dir_caps = 1004

slot_player_unblockable_warnings = 1000
slot_player_autoblock_warnings = 1001
slot_player_aimbot_warnings = 1002

slot_item_num_attacks = 1000

slot_agent_tick_check_time = 1000
slot_agent_defend_dir = 1001
slot_agent_defend_ticks = 1002

slot_agent_period_reset_time = 1003

slot_agent_period_melee_hits = 1004
slot_agent_period_blocks = 1005
slot_agent_period_ranged_hits = 1006

slot_agent_period_unblocks = 1007
slot_agent_period_down_blocks = 1008
slot_agent_period_head_shots = 1009
#MBAC end
