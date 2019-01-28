from ud4d.detector import UDevDetector
from ud4d.event import UEvent, UEventManager
from ud4d.api import safe_ud4d, start_ud4d, stop_ud4d

import time


if __name__ == '__main__':
    # simple way
    start_ud4d()
    time.sleep(20)
    stop_ud4d()

    # or do wtf you want
    with safe_ud4d():
        for _ in range(32):
            first_event = UDevDetector.read_event()
            event_object = UEvent(first_event)
            UEventManager.add_event(event_object)

            action_name = event_object.get_action_name()
            # less log
            if action_name in ('bind', 'unbind'):
                dev_name = event_object.get_dev_name()
                event_id = event_object.get_event_id()
                print({
                    'event id': event_id,
                    'action': action_name,
                    'dev name': dev_name,
                })

                current_event_dict = UEventManager.get_event_dict()
                print(current_event_dict)
