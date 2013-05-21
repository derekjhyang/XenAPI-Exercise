import XenAPI, sys

def main(session):
    try:
        # Register for events on all classes:
        session.xenapi.event.register(["*"])
        while True:
            try:
                events = session.xenapi.event.next()

                # Print the events out in a nice format:
                fmt = "%8s  %20s  %5s  %s"
                hdr = fmt % ("id", "class", "type", "name of object (if available)")
                print "-" * (len(hdr))
                print hdr
                print "-" * (len(hdr))
                for event in events:
                    name = "(unknown object name)"
                    if "snapshot" in event.keys():
                        snapshot = event['snapshot']
                        if "name_label" in snapshot.keys():
                            name = snapshot['name_label']
                    print fmt % (event['id'], event['class'], event['operation'], name)

            except XenAPI.Failure, e:
                if e.details <> [ "EVENTS_LOST" ]: raise
                print "** Caught EVENTS_LOST error: some events may be lost"
                # Check for the "EVENTS_LOST" error (happens if the event queue fills up on the
                # server and some events have been lost). The only thing we can do is to
                # unregister and then re-register again for future events.
                # NB: A program which is waiting for a particular condition to become true would
                # need to explicitly poll the state to make sure the condition hasn't become
                # true in the gap.
                session.xenapi.event.unregister(["*"])
                session.xenapi.event.register(["*"])
    finally:
        session.xenapi.session.logout()


if __name__ == "__main__":
    if len(sys.argv) <> 4:
        print "Usage:"
        print sys.argv[0], " <url> <username> <password>"
        sys.exit(1)
    url = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    # First acquire a valid session by logging in:
    session = XenAPI.Session(url)
    session.xenapi.login_with_password(username, password)
    main(session)
