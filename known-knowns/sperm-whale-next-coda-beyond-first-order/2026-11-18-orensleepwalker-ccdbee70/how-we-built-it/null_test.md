# Dialogue scorer null comparison
controls: 800
best_control: 0.100664285462306
real: 0.130409563589848
real_beats_all_controls: yes
command: python3 code/controls.py dialogues payload; python3 code/controls.py dialogues first_order; python3 code/summarize_campaign.py --save

The displayed scalar is the lesser of the model's two gains after subtracting the applicable full-win threshold from each. Each of the two gains individually also exceeds all matched-control gains. See the two 400-seed logs and the separate all-family sensitivity in output/decision.json. These results are for the model-selection rule frozen before evaluation.
