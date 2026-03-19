from datetime import datetime
from collections import defaultdict

def find_free_slots(entries):
    timetable = defaultdict(list)

    # group by day
    for entry in entries:
        timetable[entry.day].append(entry)

    result = []

    for day, classes in timetable.items():
        time_blocks = []

        for entry in classes:
            start = datetime.strptime(entry.start_time, "%H:%M")
            end = datetime.strptime(entry.end_time, "%H:%M")
            time_blocks.append((start, end))

        # sort classes
        time_blocks.sort(key=lambda x: x[0])

        free_slots = []

        day_start = datetime.strptime("09:00", "%H:%M")
        day_end = datetime.strptime("17:00", "%H:%M")

        # gap before first class
        if time_blocks and time_blocks[0][0] > day_start:
            free_slots.append({
                "start": day_start.strftime("%H:%M"),
                "end": time_blocks[0][0].strftime("%H:%M")
            })

        # gaps between classes
        for i in range(len(time_blocks) - 1):
            current_end = time_blocks[i][1]
            next_start = time_blocks[i + 1][0]

            if next_start > current_end:
                free_slots.append({
                    "start": current_end.strftime("%H:%M"),
                    "end": next_start.strftime("%H:%M")
                })

        # gap after last class
        if time_blocks and time_blocks[-1][1] < day_end:
            free_slots.append({
                "start": time_blocks[-1][1].strftime("%H:%M"),
                "end": day_end.strftime("%H:%M")
            })

        result.append({
            "day": day,
            "free_slots": free_slots
        })

    return result