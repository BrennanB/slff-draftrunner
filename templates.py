def new_draft(start_date, start_time, close_date, close_time, team_list, short_name):

    new_draft = "Draft will be run on [date={} time={} timezone=\"America/Toronto\"] . " \
            "Signups close [date={} time={} timezone=\"America/Toronto\"] .\n\n# Draft Info\n\n" \
            "This is currently a semi-automated draft runner, and there may be bugs, timing will be 2/2/2.\n\n[details=\"Team List\"]\n{}\n[/details]\n\n" \
            "Like this post to sign up, and send all the lists to my beautiful bot self! Make the title of your PM for lists '{}'".format(start_date, start_time, close_date, close_time, team_list, short_name)
    return new_draft