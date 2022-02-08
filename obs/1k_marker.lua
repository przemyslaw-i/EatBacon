-- Parameters variables (do not change)
obs           = obslua
distance_file = ""
source_name   = ""
shown         = false
started       = false
last_distance = 0.0
threshold     = 100
check_time    = 2
decay         = 5

--
-- This part is providing main functionality
--

function visibility_change(visible)
    -- Get/lock scene and find source in the scene.
    local current_scene = obs.obs_scene_from_source(obs.obs_frontend_get_current_scene())
    scene_item = obs.obs_scene_find_source(current_scene, source_name)

    -- Set element visibility and release the scene.
    obs.obs_sceneitem_set_visible(scene_item, visible)
    obs.obs_scene_release(current_scene)
end

function show_timer_callback()
    -- Change visibility of the item and stop the timer
    obs.remove_current_callback()
    shown = false
    visibility_change(false)
end

function check_timer_callback()
    -- Read distance file 
    local file = io.open(distance_file, "rb")

    -- If failed to load file, skip
    if not file then
        print("Cannot open file...")
        return nil
    end

    -- Read and parse the file. If failed, skip
    local content = tonumber(file:read "*a")
    file:close()
    if not content then
        print("Cannot parse value...")
        return nil
    end

    -- Check if current value is >= than threshold.
    if ((content - last_distance) > 0) and ((content - last_distance) >= threshold) then
        print(string.format("%02.2f, %02.2f, %02.2f", content, last_distance, threshold))
        -- If so, save new threshold
        last_distance = content

        -- If element is not yet started
        if not shown then
            -- Change element visibility
            visibility_change(true)
            shown = true

            -- Set timer to hide the element
            obs.timer_add(show_timer_callback, decay)
            print("Threshold reached!")
        end
    else
        print("Threshold not reached...")
    end
end

function start_stop_toggle()
    -- This function starts/stops whole logic
    if started then
        obs.timer_remove(check_timer_callback)
        started = false
        print("Logic stopped.")
    else
        started = true
        obs.timer_add(check_timer_callback, check_time)
        print("Logic started.")
    end
end

--
-- This part is providing configuration parameters for this script
--

function script_update(settings)
    -- Parameters update
    source_name = obs.obs_data_get_string(settings, "source")
    decay = obs.obs_data_get_int(settings, "decay") * 1000
    threshold = obs.obs_data_get_int(settings, "threshold")
    distance_file = obs.obs_data_get_string(settings, "file")
    check_time = obs.obs_data_get_int(settings, "check_time") * 1000 
end

function script_defaults(settings)
    -- Parameters defaults
	obs.obs_data_set_default_int(settings, "decay", 5)
	obs.obs_data_set_default_string(settings, "threshold", 100)
    obs.obs_data_set_default_string(settings, "check_time", 2)
end

function script_properties()
    -- Setup
    local props = obs.obs_properties_create()

    -- Parameters
    obs.obs_properties_add_text(props, "source", "Source", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_int(props, "decay", "Decay time", 1, 60, 1)
    obs.obs_properties_add_int(props, "threshold", "Distance threshold", 100, 1000, 100)
    obs.obs_properties_add_text(props, "file", "Distance file", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_int(props, "check_time", "File check time", 1, 10, 1)

    -- Buttons
    obs.obs_properties_add_button(props, "button", "Start/Stop", start_stop_toggle)

    -- Return
    return props
end