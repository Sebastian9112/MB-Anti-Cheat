#Add this inside the script "game_quick_start"
#MBAC begin
(call_script, "script_mbac_init"),
#MBAC end

#Add this inside the script "game_get_console_command", after the second (try_begin)
#MBAC begin
      (call_script, "script_cf_mbac_console_command", ":input", ":val1"),
    (else_try),
#MBAC end

#Add this to the very end
#MBAC begin
from module_items import items

attack_dir_caps = [
#down
  itcf_thrust_onehanded|
  itcf_thrust_twohanded|
  itcf_thrust_polearm|
  itcf_horseback_thrust_onehanded|
  itcf_thrust_onehanded_lance|
  itcf_thrust_onehanded_lance_horseback|
  itcf_thrust_musket,
#up
  itcf_overswing_onehanded|
  itcf_overswing_twohanded|
  itcf_overswing_polearm|
  itcf_horseback_overswing_right_onehanded|
  itcf_horseback_overswing_left_onehanded|
  itcf_overswing_spear|
  itcf_overswing_musket,
#right
  itcf_slashright_onehanded|
  itcf_slashright_twohanded|
  itcf_slashright_polearm|
  itcf_horseback_slashright_onehanded|
  itcf_horseback_slash_polearm,
#left
  itcf_slashleft_onehanded|
  itcf_slashleft_twohanded|
  itcf_slashleft_polearm|
  itcf_horseback_slashleft_onehanded|
  itcf_horseback_slash_polearm
]

def mbac_pre_init():
  objects = []
  for i in xrange(num_hacks):
    objects.append((troop_set_slot, i, slot_troop_enable_anti_cheat, hack_detection[i]))
    objects.append((troop_set_slot, i, slot_troop_hack_percentage, hack_percentage[i]))
    objects.append((troop_set_slot, i, slot_troop_hack_consequence, hack_consequence[i]))
    objects.append((troop_set_slot, i, slot_troop_hack_warn_threshold, hack_warn_threshold[i]))
  for i in xrange(len(attack_dir_caps)):
    objects.append((troop_set_slot, i, slot_troop_item_attack_dir_caps, attack_dir_caps[i]))
  return objects[:]

scripts += [
  ("mbac_pre_init", mbac_pre_init()),

  ("mbac_init", [
    (call_script, "script_mbac_pre_init"),

    (assign, "$first_player_joined", 0),

    (assign, "$advanced_logging", 1),#logs plenty of data for later parameter fine-tuning
    (assign, "$player_join_message", 1),#sends the joining player a message that this server is unsing anti cheat
    (assign, "$broadcast_hack_warnings", msg_admins),
    (assign, "$broadcast_hack_consequences", msg_players),

    (assign, "$hack_check_period", 30000),#miliseconds
    (assign, "$warnings_til_consequences", 3),#warnings til consequence

    #check for attack directions
    (try_for_range, ":item", 0, len(items)),
      (item_get_type, ":item_type", ":item"),
      (is_between, ":item_type", itp_type_one_handed_wpn, itp_type_arrows),
      (assign, ":num_attacks", 0),
      (try_for_range, ":i", 0, 4),
        (troop_get_slot, ":capability", ":i", slot_troop_item_attack_dir_caps),
        (item_has_capability, ":item", ":capability"),
        (val_add, ":num_attacks", 1),
      (try_end),
      (item_set_slot, ":item", slot_item_num_attacks, ":num_attacks"),
    (try_end),
  ]),

  ("cf_mbac_console_command", [
    (store_script_param, ":command", 1),
    (store_script_param, ":value", 2),

    #reuse class limiter commands and values
    (val_sub, ":command", 66),
    (val_sub, ":value", 102),#allows for -1

    (str_clear, s0),
    (try_begin),
      (eq, ":command", cmd_advanced_logging),
      (is_between, ":value", 0, 2),
      (assign, "$advanced_logging", ":value"),

      (store_add, ":string", "str_hack_option_0", ":value"),
      (str_store_string, s1, ":string"),
      (str_store_string, s0, "@Advanced logging {s1}"),

    (else_try),
      (eq, ":command", cmd_player_join_message),
      (is_between, ":value", 0, 2),
      (assign, "$player_join_message", ":value"),

      (store_add, ":string", "str_hack_option_0", ":value"),
      (str_store_string, s1, ":string"),
      (str_store_string, s0, "@Player join message {s1}"),

    (else_try),
      (eq, ":command", cmd_broadcast_hack_warnings),
      (is_between, ":value", -1, 2),
      (assign, "$broadcast_hack_warnings", ":value"),

      (store_add, ":string", "str_hack_broadcast_option_0", ":value"),
      (str_store_string, s1, ":string"),
      (str_store_string, s0, "@Hack-warning message set to {s1}"),

    (else_try),
      (eq, ":command", cmd_broadcast_hack_consequences),
      (is_between, ":value", -1, 2),
      (assign, "$broadcast_hack_consequences", ":value"),

      (store_add, ":string", "str_hack_broadcast_option_0", ":value"),
      (str_store_string, s1, ":string"),
      (str_store_string, s0, "@Hack-consequences message set to {s1}"),

    (else_try),
      (is_between, ":command", cmd_hacks_option, cmd_hacks_consequence),
      (is_between, ":value", 0, 2),
      (val_sub, ":command", cmd_hacks_option),
      (troop_set_slot, ":command", slot_troop_enable_anti_cheat, ":value"),

      (store_add, ":string", "str_hack_option_0", ":value"),
      (str_store_string, s1, ":string"),
      (store_add, ":string", "str_hack_0", ":command"),
      (str_store_string, s2, ":string"),
      (str_store_string, s0, "@{s2} detection {s1}"),

    (else_try),
      (is_between, ":command", cmd_hacks_consequence, cmd_end),
      (is_between, ":value", -1, 3),
      (val_sub, ":command", cmd_hacks_consequence),
      (troop_set_slot, ":command", slot_troop_hack_consequence, ":value"),

      (store_add, ":string", "str_hack_consequence_option_0", ":value"),
      (str_store_string, s1, ":string"),
      (store_add, ":string", "str_hack_0", ":command"),
      (str_store_string, s2, ":string"),
      (str_store_string, s0, "@{s2} hack consequence set to {s1}"),
    (try_end),

    (neg|str_is_empty, s0),
  ]),

  ("mbac_init_player", [
    (store_script_param, ":player", 1),

    (try_for_range, ":slot", slot_player_unblockable_warnings, slot_player_unblockable_warnings + num_hacks),
      (player_set_slot, ":player", ":slot", 0),
    (try_end),
  ]),

  ("mbac_set_up_message", [
    (store_script_param, ":msg_type", 1),

    (try_begin),
      (neq, ":msg_type", msg_log_only),
      (try_for_players, ":player", "$is_dedi"),
        (try_begin),
          (eq, ":msg_type", msg_players),
          (multiplayer_send_string_to_player, ":player", multiplayer_event_show_server_message, s0),
        (else_try),
          (player_is_admin, ":player"),
          (multiplayer_send_string_to_player, ":player", multiplayer_event_show_server_message, s0),
        (try_end),
      (try_end),
    (try_end),

    #logging
    (assign, reg61, mbac_v_maj),
    (assign, reg62, mbac_v_min),
    (assign, reg63, mbac_v_rev),
    (str_store_string, s0, "@[MBAC v{reg61}.{reg62}.{reg63}]: {s0}"),
    (try_begin),
      (eq, "$is_dedi", 1),
      (server_add_message_to_log, s0),
    (else_try),
      (display_message, s0),
    (try_end),
  ]),

  ("mbac_hack_consequence", [
    (store_script_param, ":player", 1),

    (assign, ":hack_consequence", con_message),
    (assign, ":hack_count", 0),
    (try_for_range, ":i", 0, num_hacks),
      (store_add, ":slot", slot_player_unblockable_warnings, ":i"),
      (player_slot_ge, ":player", ":slot", "$warnings_til_consequences"),
      (val_add, ":hack_count", 1),
      (store_add, ":string", "str_hack_0", ":i"),
      (try_begin),
        (eq, ":hack_count", 1),
        (str_store_string, s0, ":string"),
      (else_try),
        (str_store_string, s1, ":string"),
        (str_store_string, s0, "@{s0}, {s1}"),
      (try_end),

      (troop_get_slot, ":cur_consequence", ":i", slot_troop_hack_consequence),
      (gt, ":cur_consequence", con_message),
      (try_begin),
        (eq, ":hack_consequence", con_message),
        (assign, ":hack_consequence", ":cur_consequence"),
      (else_try),#check for consequence hierarchy
        (lt, ":cur_consequence", ":hack_consequence"),
        (assign, ":hack_consequence", ":cur_consequence"),
      (try_end),
    (try_end),

    (store_add, ":string", "str_hack_consequence_0", ":hack_consequence"),
    (str_store_string, s1, ":string"),
    (str_store_string, s0, "@got {s1} for using cheats({s0})"),

    (str_store_player_username, s1, ":player"),
    (player_get_unique_id, reg0, ":player"),
    (str_store_string, s0, "@Player {s1} with UID {reg0} {s0}"),

    (call_script, "script_mbac_set_up_message", "$broadcast_hack_consequences"),

    (try_begin),#notification only
      (this_or_next|player_is_admin, ":player"),
      (eq, ":hack_consequence", con_message),
      (call_script, "script_mbac_init_player", ":player"),
    (else_try),#ban
      (is_between, ":hack_consequence", con_perma_ban, con_temp_ban + 1),
      (ban_player, ":player", ":hack_consequence", 0),
      (save_ban_info_of_player, ":player"),
    (else_try),#kick
      (kick_player, ":player"),
    (try_end),
  ]),

  ("cf_mbac_ti_player_joined", [
    (store_trigger_param, ":player", 1),
    
    (call_script, "script_mbac_init_player", ":player"),
    (try_begin),
      (eq, "$player_join_message", 1),
      (this_or_next|eq, "$first_player_joined", 0),
      (player_slot_ge, ":player", slot_player_join_time, 5),#not on map change

      (assign, reg0, mbac_v_maj),
      (assign, reg1, mbac_v_min),
      (assign, reg2, mbac_v_rev),
      (str_store_string, s0, "@This server is using MB Anti Cheat v{reg0}.{reg1}.{reg2}"),
      (multiplayer_send_string_to_player, ":player", multiplayer_event_show_server_message, s0),
    (try_end),

    (eq, "$first_player_joined", 0),
    (assign, "$first_player_joined", 1),
  ]),

  ("cf_mbac_ti_mission_end", [
    (multiplayer_is_server),
    (try_for_players, ":player", "$is_dedi"),
      (call_script, "script_mbac_init_player", ":player"),
    (try_end),
  ]),

  ("cf_mbac_ti_agent_spawn", [
    (store_trigger_param, ":agent", 1),

    (agent_is_human, ":agent"),
    (store_mission_timer_a_msec, ":time"),
    (store_random_in_range, ":check_time", 0, 100),#randomize check time within 0.1 sec
    (val_add, ":check_time", ":time"),
    (agent_set_slot, ":agent", slot_agent_tick_check_time, ":check_time"),
    (agent_set_slot, ":agent", slot_agent_defend_dir, -1),

    (neg|agent_is_non_player, ":agent"),#only players
    (store_random_in_range, ":check_time", 0, "$hack_check_period"),#randomize reset time
    (val_add, ":check_time", ":time"),
    (agent_set_slot, ":agent", slot_agent_period_reset_time, ":check_time"),
  ]),

  ("cf_mbac_ti_agent_hit", [
    (store_trigger_param, ":v_agent", 1),
    (store_trigger_param, ":d_agent", 2),
    (store_trigger_param, ":v_bone", 4),
    (assign, ":d_item", reg0),

    (neg|agent_is_non_player, ":d_agent"),
    (agent_is_human, ":v_agent"),

    (neq, ":d_item", -1),
    (item_get_type, ":item_type", ":d_item"),

    (try_begin),#melee
      (is_between, ":item_type", itp_type_one_handed_wpn, itp_type_arrows),
      #unblockable detection
      (try_begin),
        (troop_slot_eq, hack_unblockable, slot_troop_enable_anti_cheat, 1),

        (agent_get_slot, ":hits", ":d_agent", slot_agent_period_melee_hits),
        (val_add, ":hits", 1),
        (agent_set_slot, ":d_agent", slot_agent_period_melee_hits, ":hits"),

        (item_get_slot, ":num_attacks", ":d_item", slot_item_num_attacks),
        (is_between, ":num_attacks", 1, 4),#exclude melee weapons with no, or 4 valid attack directions
        (agent_get_defend_action, ":defend_action", ":v_agent"), #returned values: free = 0, parrying = 1, blocking = 2
        (neq, ":defend_action", 0),

        (agent_get_action_dir, ":v_dir", ":v_agent"), #invalid = -1, down = 0, right = 1, left = 2, up = 3
        (agent_get_action_dir, ":d_dir", ":d_agent"), #invalid = -1, down = 0, right = 1, left = 2, up = 3
        (eq, ":v_dir", ":d_dir"),

        (agent_get_slot, ":defend_ticks", ":v_agent", slot_agent_defend_ticks),
        (gt, ":defend_ticks", 1),

        (agent_get_animation, ":v_anim", ":v_agent", 0),
        (neq, ":v_anim", "anim_kick_right_leg"),

        (assign, ":crush_check", 1),
        (try_begin),
          (eq, ":d_dir", 3),
          (item_has_property, ":d_item", itp_crush_through),
          (assign, ":crush_check", 0),
        (try_end),
        (eq, ":crush_check", 1),

        (agent_get_position, pos1, ":v_agent"),
        (agent_get_position, pos2, ":d_agent"),
        (neg|position_is_behind_position, pos2, pos1),

        (set_fixed_point_multiplier, 1),
        (get_angle_between_positions, ":angle", pos1, pos2),
        (set_fixed_point_multiplier, 100),

        (val_abs, ":angle"),# 180 = face to face
        (gt, ":angle", 105),

        (agent_get_slot, ":hits", ":d_agent", slot_agent_period_unblocks),
        (val_add, ":hits", 1),
        (agent_set_slot, ":d_agent", slot_agent_period_unblocks, ":hits"),

        # (set_trigger_result, 0),

        #logging
        (try_begin),
          (eq, "$advanced_logging", 1),
          (agent_get_player_id, ":player", ":d_agent"),
          (str_store_player_username, s0, ":player"),
          (player_get_unique_id, reg1, ":player"),
          (assign, reg2, ":hits"),
          (assign, reg3, ":angle"),
          (get_distance_between_positions, reg4, pos1, pos2),
          (assign, reg5, ":defend_action"),
          (assign, reg6, ":v_dir"),
          (assign, reg7, ":num_attacks"),
          (assign, reg8, ":defend_ticks"),
          (str_store_string, s0, "@Player:{s0} UID:{reg1} [period_unblocks({reg2}) angle({reg3}) dist({reg4}) defend({reg5}) dir({reg6}) num_att({reg7}) def_ticks({reg8})]"),
          (call_script, "script_mbac_set_up_message", msg_log_only),
        (try_end),
      (try_end),

    (else_try),#ranged
      (troop_slot_eq, hack_aimbot, slot_troop_enable_anti_cheat, 1),

      (agent_get_slot, ":hits", ":d_agent", slot_agent_period_ranged_hits),
      (val_add, ":hits", 1),
      (agent_set_slot, ":d_agent", slot_agent_period_ranged_hits, ":hits"),

      (eq, ":v_bone", 9),#head
      (agent_get_slot, ":hits", ":d_agent", slot_agent_period_head_shots),
      (val_add, ":hits", 1),
      (agent_set_slot, ":d_agent", slot_agent_period_head_shots, ":hits"),
    (try_end),
  ]),

  ("cf_mbac_ti_once", [
    (multiplayer_is_server),
    (try_begin),
      (multiplayer_is_dedicated_server),
      (assign, "$is_dedi", 1),
    (else_try),
      (assign, "$is_dedi", 0),
    (try_end),
  ]),

  ("cf_mbac_ti_each_frame", [
    (multiplayer_is_server),
    (store_mission_timer_a_msec, ":time"),
    (server_get_control_block_dir, ":cbd"),

    (try_for_agents, ":agent", 0, 0),
      (agent_is_alive, ":agent"),
      (agent_is_human, ":agent"),
      (agent_get_slot, ":check_time", ":agent", slot_agent_tick_check_time),
      (try_begin),
        (ge, ":time", ":check_time"),#check agents in batches, splits the workload across as many frames as possible
        (val_add, ":check_time", 100),
        (agent_set_slot, ":agent", slot_agent_tick_check_time, ":check_time"),
        (agent_get_defend_action, ":defend", ":agent"), #returned values: free = 0, parrying = 1, blocking = 2
        (try_begin),
          (eq, ":defend", 2),
          (agent_get_action_dir, ":dir", ":agent"), #invalid = -1, down = 0, right = 1, left = 2, up = 3
          (agent_set_slot, ":agent", slot_agent_defend_dir, ":dir"),
          (agent_get_slot, ":ticks", ":agent", slot_agent_defend_ticks),
          (val_add, ":ticks", 1),
          (agent_set_slot, ":agent", slot_agent_defend_ticks, ":ticks"),
          (try_begin),
            (troop_slot_eq, hack_autoblock, slot_troop_enable_anti_cheat, 1),
            (neg|agent_is_non_player, ":agent"),#only players

            (eq, ":ticks", 1),#count only once per block
            (agent_get_slot, ":blocks", ":agent", slot_agent_period_blocks),
            (val_add, ":blocks", 1),
            (agent_set_slot, ":agent", slot_agent_period_blocks, ":blocks"),

            (eq, ":cbd", 1),#manual block enabled
            (eq, ":dir", 0),#down
            (agent_get_slot, ":blocks", ":agent", slot_agent_period_down_blocks),
            (val_add, ":blocks", 1),
            (agent_set_slot, ":agent", slot_agent_period_down_blocks, ":blocks"),
          (try_end),
        (else_try),
          (agent_set_slot, ":agent", slot_agent_defend_dir, -1),
          (agent_set_slot, ":agent", slot_agent_defend_ticks, 0),
        (try_end),
      (try_end),

      #check for hack consequences, reset period logs
      (neg|agent_is_non_player, ":agent"),#only players
      (agent_get_slot, ":check_time", ":agent", slot_agent_period_reset_time),
      (ge, ":time", ":check_time"),#check agents in batches, splits the workload across as many frames as possible
      (val_add, ":check_time", "$hack_check_period"),
      (agent_set_slot, ":agent", slot_agent_period_reset_time, ":check_time"),

      (agent_get_player_id, ":player", ":agent"),
      (assign, ":message", 0),

      (try_begin),
        (eq, "$advanced_logging", 1),
        (str_clear, s0),
      (try_end),

      (try_for_range, ":i", 0, num_hacks),
        (troop_slot_eq, ":i", slot_troop_enable_anti_cheat, 1),

        (store_add, ":slot", slot_agent_period_unblocks, ":i"),
        (agent_get_slot, ":incidents", ":agent", ":slot"),
        (agent_set_slot, ":agent", ":slot", 0),#reset

        (store_add, ":slot", slot_agent_period_melee_hits, ":i"),
        (agent_get_slot, ":total", ":agent", ":slot"),
        (agent_set_slot, ":agent", ":slot", 0),#reset

        (this_or_next|eq, "$advanced_logging", 1),
        (neg|troop_slot_ge, ":i", slot_troop_hack_warn_threshold, ":incidents"),

        (try_begin),
          (gt, ":total", 0),
          (store_mul, ":cur_percentage", ":incidents", 100),
          (val_div, ":cur_percentage", ":total"),
        (else_try),
          (assign, ":cur_percentage", 0),
        (try_end),

        (try_begin),
          (eq, "$advanced_logging", 1),
          (neq, ":incidents", 0),
          (assign, reg0, ":total"),
          (assign, reg1, ":incidents"),
          (assign, reg2, ":cur_percentage"),
          (store_add, ":string", "str_hack_0_log", ":i"),
          (str_store_string, s1, ":string"),
          (str_store_string, s0, "@{s0}, {s1}"),
        (try_end),

        (neg|troop_slot_ge, ":i", slot_troop_hack_warn_threshold, ":incidents"),
        (neg|troop_slot_ge, ":i", slot_troop_hack_percentage, ":cur_percentage"),

        (store_add, ":slot", slot_player_unblockable_warnings, ":i"),
        (player_get_slot, ":warnings", ":player", ":slot"),
        (try_begin),
          (lt, ":warnings", "$warnings_til_consequences"),
          (val_add, ":warnings", 1),
          (player_set_slot, ":player", ":slot", ":warnings"),
          (try_begin),
            (eq, ":warnings", "$warnings_til_consequences"),
            (assign, ":message", 2),
          (else_try),
            (neq, ":message", 2),
            (assign, ":message", 1),
          (try_end),
        (else_try),
          (assign, ":message", 2),
        (try_end),
      (try_end),

      (try_begin),
        (this_or_next|eq, "$advanced_logging", 1),
        (eq, ":message", 1),
        (str_store_player_username, s1, ":player"),
        (player_get_unique_id, reg0, ":player"),
      (try_end),

      (try_begin),
        (eq, "$advanced_logging", 1),
        (neg|str_is_empty, s0),
        (str_store_string, s0, "@Player:{s1} UID:{reg0} {s0}"),
        (call_script, "script_mbac_set_up_message", msg_log_only),
      (try_end),

      (try_begin),#admin notification
        (eq, ":message", 1),
        (str_store_string, s0, "@Player {s1} with UID {reg0} might be using cheats"),
        (try_for_range, ":i", 0, num_hacks),
          (store_add, ":string", "str_hack_0", ":i"),
          (str_store_string, s1, ":string"),
          (store_add, ":slot", slot_player_unblockable_warnings, ":i"),
          (player_get_slot, reg0, ":player", ":slot"),
          (gt, reg0, 0),
          (assign, reg1, "$warnings_til_consequences"),
          (str_store_string, s0, "@{s0} {s1}({reg0}/{reg1})"),
        (try_end),
        (call_script, "script_mbac_set_up_message", "$broadcast_hack_warnings"),
      (else_try),#consequence
        (eq, ":message", 2),
        (call_script, "script_mbac_hack_consequence", ":player"),
      (try_end),
    (try_end),
  ]),
]
#MBAC end
