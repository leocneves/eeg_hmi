
function initialize(box)

	dofile(box:get_config("${Path_Data}") .. "/plugins/stimulation/lua-stimulator-stim-codes.lua")

	start_time = box:get_setting(2)
	video_time = box:get_setting(3)
	question_time = box:get_setting(4)
	rest_time = box:get_setting(5)
	number_of_trials = box:get_setting(6)
	first_class = _G[box:get_setting(7)]
	second_class = _G[box:get_setting(8)]

	-- initializes random seed
	math.randomseed(os.time())

	-- fill the sequence table with predifined order
	sequence = {}
	for i = 1, number_of_trials do
		table.insert(sequence, 1, first_class)
		table.insert(sequence, 1, second_class)
	end

	-- randomize the sequence
	for i = 1, number_of_trials do
		a = math.random(1, number_of_trials)
		b = math.random(1, number_of_trials)
		swap = sequence[a]
		sequence[a] = sequence[b]
		sequence[b] = swap
	end

end

function process(box)

	local t=0

	-- manages baseline
	box:send_stimulation(1, OVTK_StimulationId_ExperimentStart, t, 0)
	t = t + 5

	-- manages trials

	for i = 1, number_of_trials do

		-- black to start
		box:send_stimulation(1, OVTK_GDF_Start_Of_Trial, t, 0)
		t = t + start_time

		-- display video clip
		box:send_stimulation(1, sequence[i], t, 0)
		t = t + video_time

		-- questions
		box:send_stimulation(1, OVTK_StimulationId_NonTarget, t, 0)
		t = t + question_time

		-- Rest time
		if not i == number_of_trials then
			box:send_stimulation(1, OVTK_StimulationId_RestStart, t, 0)
			t = t + rest_time
		end

	end

	-- send end for completeness	
	box:send_stimulation(1, OVTK_GDF_End_Of_Session, t, 0)
	t = t + 5

	box:send_stimulation(1, OVTK_StimulationId_Train, t, 0)
	t = t + 1
	
	-- used to cause the acquisition scenario to stop
	box:send_stimulation(1, OVTK_StimulationId_ExperimentStop, t, 0)
	
end
