import pickle

sessions = pickle.load(open('gesture_time.data', 'r'))
csv_file = open('gesture_time.csv', 'w')
for user in sessions:
    trial_num = 0
    for trial in sessions[user]:
        csv_file.write("%s, %s, %s,"%(user, trial_num, len(trial)))
        for time in trial:
            csv_file.write("%f,"%time)
        csv_file.write("\n")
csv_file.close()