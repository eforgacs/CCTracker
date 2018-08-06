import WorkoutEngine as we

ccengine = we.CCEngine()
ed_rec = we.Record("Ed")

current_workout = ccengine.next_workout(we.WorkoutType.pushups, ed_rec)

    # for all exercises
    #interactive/print workout
ed_rec.record_workout(current_workout)

ed_rec.record()
