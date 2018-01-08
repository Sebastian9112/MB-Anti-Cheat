mb_anti_cheat = [
(ti_on_agent_hit, 0, 0, [],
[
    (store_trigger_param_1, ":victim_agent"),
    (store_trigger_param_2, ":dealer_agent"),

    (neg|agent_is_non_player, ":dealer_agent"),
    (agent_is_human, ":victim_agent"),

    (neq, reg0, -1),
    (item_get_type, ":item_type", reg0),
    (is_between, ":item_type", itp_type_one_handed_wpn, itp_type_arrows),

    (agent_get_defend_action, ":defend_action", ":victim_agent"), #returned values: free = 0, parrying = 1, blocking = 2
    (neq, ":defend_action", 0),

    (agent_get_action_dir, ":v_dir", ":victim_agent"), #invalid = -1, down = 0, right = 1, left = 2, up = 3
    (agent_get_action_dir, ":d_dir", ":dealer_agent"), #invalid = -1, down = 0, right = 1, left = 2, up = 3
    (eq, ":v_dir", ":d_dir"),

    (agent_get_animation, ":v_anim", ":victim_agent", 0),
    (neq, ":v_anim", "anim_kick_right_leg"),

    (assign, ":crush_check", 1),
    (try_begin),
        (eq, ":d_dir", 3),
        (item_has_property, reg0, itp_crush_through),
        (assign, ":crush_check", 0),
    (try_end),
    (eq, ":crush_check", 1),

    (agent_get_position, pos1, ":victim_agent"),
    (agent_get_position, pos2, ":dealer_agent"),
    (neg|position_is_behind_position, pos2, pos1),

    (set_fixed_point_multiplier, 1),
    (get_angle_between_positions, ":angle", pos1, pos2),
    (set_fixed_point_multiplier, 100),

    (val_abs, ":angle"),# 180 = face to face
    (gt, ":angle", 105),

    (agent_get_player_id, ":player", ":dealer_agent"),
    (str_store_player_username, s0, ":player"),
    (player_get_unique_id, reg1, ":player"),
    (str_store_string, s0, "@{s0} with UID {reg1} might be using unblockable attacks"),
    (server_add_message_to_log, s0),

    (try_for_players, ":cur_player", 1),
        (player_is_admin, ":cur_player"),
        (multiplayer_send_string_to_player, ":cur_player", multiplayer_event_show_server_message, s0),
    (try_end),
    
    # (ban_player, ":player", 0, 0),
    # (save_ban_info_of_player, ":player"),
    
    (set_trigger_result, 0),
]),
]
