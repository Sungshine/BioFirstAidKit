import csv
import time
import datetime
import calendar

# Read in file
# Removed duplicate jobid entries & jobids where sub-time > start-time
# f = '/Users/sim/Desktop/HPCaccounting.txt'
# f = '/Users/sim/Desktop/HPCaccounting_trim1.txt'
# f = '/Users/sim/Desktop/HPCaccounting_trim3.txt'
f = '/Users/sim/Desktop/HPCaccounting_trim3.txt'

big_dict = {}

with open(f, 'r') as fh:
    r = csv.reader(fh, delimiter='\t')
    col_names = next(r, None)
    # print('\t'.join(col_names))
    
    for row in r:
        jobname = row[4]
        jobid = row[5]
        subtime = row[8]
        starttime = row[9]
        endtime = row[10]
        sub = datetime.datetime.fromtimestamp(int(subtime))
        start = datetime.datetime.fromtimestamp(int(starttime))
        end = datetime.datetime.fromtimestamp(int(endtime))

        if jobid not in big_dict.keys():
            big_dict[jobid] = [sub, start, end]
        else:
            print('KEY ERROR = {}'.format(jobid))
            continue


import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

# Plot submission to start time
# Link each job instance to the time it takes to start the job
job_times = []
end_times = []
for k, v in big_dict.items():
    sub = v[0]
    start = v[1]
    end = v[2]
    sub2start = start - sub
    sub2end = end - sub
    job_times.append([sub, sub2start])
    end_times.append([sub, sub2end])

# Then sort by submission datetime
sorted_job_times = sorted(job_times, key=lambda x: x[0])
sorted_end_times = sorted(end_times, key=lambda x: x[0])

# Separate job submission datetime and wait time value into corresponding lists
job_submit_times = []
times_to_start = []

for i in sorted_job_times:
    job_submit_times.append(i[0])
    times_to_start.append(i[1])

times_to_end = []
for i in sorted_end_times:
    times_to_end.append(i[1])

# While matplotlib can in principle handle datetime objects, the plot cannot interpret them directly
# So one may add an arbitrary date to the timedeltas then convert them to numbers
zero = datetime.datetime(2019, 1, 1)
times = [zero + t for t in times_to_start]
zero = mdates.date2num(zero)

values = [t - zero for t in mdates.date2num(times)]
dates = mdates.date2num(job_submit_times)

zero = datetime.datetime(2019, 1, 1)
endtimes = [zero + t for t in times_to_end]
zero = mdates.date2num(zero)

values2 = [t - zero for t in mdates.date2num(endtimes)]

# Convert values (ns) to minutes
in_minutes = []
for t in times_to_start:
    a = np.timedelta64(t,'ns')
    in_minutes.append(int(str(a.astype('timedelta64[m]')).split(' ')[0]))

in_minutes2 = []
for t in times_to_end:
    a = np.timedelta64(t,'ns')
    in_minutes2.append(int(str(a.astype('timedelta64[m]')).split(' ')[0]))

# print(min(in_minutes2), max(in_minutes2), max(in_minutes2)/5)
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 10))
ax.plot(dates, values, linewidth=0.5)
# ax.plot(dates, values2, color='olive', linestyle='dashed', linewidth=0.5)
myfmt = mdates.DateFormatter('%A (%m/%d)')
ax.xaxis.set_major_formatter(myfmt)
for ax in fig.axes:
    plt.sca(ax)
    plt.xticks(rotation=45)
    plt.xticks(np.arange(min(dates), max(dates), 1.0))
    locs, labs = plt.yticks()
    print(locs, labs)
    s = [0., 0.1, 0.2, 0.3, 0.4, 0.5]
    plt.yticks(np.arange(min(s), max(s), 0.1), ('0', '100', '200', '300', '400', '0.5'))
    
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(7) 


print(max(times_to_start))
# make plot
# plt.plot(dates, values)
# plt.savefig('/Users/sim/Desktop/sub2start.png')
plt.show()















# f = '/Users/sim/Desktop/HPCaccounting_trim2.txt'

# big_dict = {}

# with open(f, 'r') as fh:
#     r = csv.reader(fh, delimiter='\t')
#     col_names = next(r, None)
#     # print('\t'.join(col_names))
    
#     for row in r:
#         qname = row[0]                                  # QNAME
#         hostname = row[1].split('-')[-1].split('.')[0]  # HOSTNAME
#         jobname = row[4]                                # JOB_NAME
#         jobid = row[5]                                  # JOB#
#         subtime = row[8]                                # SUB_TIME
#         starttime = row[9]                              # START_TIME
#         endtime = row[10]                               # END_TIME
#         failed = row[11]                                # FAILED
#         exitstat = row[12]                              # EXIT_STAT
#         runtime = row[13]                               # RUN_TIME
#         ru_utime = row[14]                              # RU_UTIME - the time the process(es) spent running in user space
#         slots = row[32]                                 # slots
#         cpu = row[33]                                   # cpu
#         mem = row[34]                                   # mem
#         io = row[35]                                    # io
#         category = row[36]                              # category
#         sub_time = row[43]                              # SUB_TIME
#         start_time = row[44]                            # START_TIME
#         end_time = row[45]                              # END_TIME
#         sub2start = row[46]                             # sub2start
#         start2end = row[47]                             # start2end
#         sub2end = row[48]                               # sub2end
#         sub = datetime.datetime.fromtimestamp(int(subtime))
#         start = datetime.datetime.fromtimestamp(int(starttime))
#         end = datetime.datetime.fromtimestamp(int(endtime))

#         if jobid not in big_dict.keys():
#             big_dict[jobid] = [sub, start, end]
#         else:
#             print('KEY ERROR = {}'.format(jobid))
#             continue

        # print(datetime.datetime.strptime(str(sub), '%Y-%m-%d %H:%M:%S'))
        # print(type(sub))
        # exit()




# qname = row[0]                                  # QNAME
        # hostname = row[1].split('-')[-1].split('.')[0]  # HOSTNAME
        # jobname = row[4]                                # JOB_NAME
        # jobid = row[5]                                  # JOB#
        # subtime = row[8]                                # SUB_TIME
        # starttime = row[9]                              # START_TIME
        # endtime = row[10]                               # END_TIME
        # failed = row[11]                                # FAILED
        # exitstat = row[12]                              # EXIT_STAT
        # runtime = row[13]                               # RUN_TIME
        # ru_utime = row[14]                              # RU_UTIME - the time the process(es) spent running in user space
        # slots = row[32]                                 # slots
        # cpu = row[33]                                   # cpu
        # mem = row[34]                                   # mem
        # io = row[35]                                    # io
        # category = row[36]                              # category
        # sub_time = row[43]                              # SUB_TIME
        # start_time = row[44]                            # START_TIME
        # end_time = row[45]                              # END_TIME
        # sub2start = row[46]                             # sub2start
        # start2end = row[47]                             # start2end
        # sub2end = row[48]                               # sub2end


        ## Printing trimmed files
        # sub = datetime.datetime.fromtimestamp(int(subtime))
        # start = datetime.datetime.fromtimestamp(int(starttime))
        # end = datetime.datetime.fromtimestamp(int(endtime))
        # sub2start = start - sub
        # start2end = end - start
        # sub2end = end - sub
        # if sub > start:
        #     continue
        # else:
        #     out = row[:43] + [str(sub), str(start), str(end), str(sub2start), str(start2end), str(sub2end)]
        #     print('\t'.join(out))


# JobID, JobName, NodeId, 
