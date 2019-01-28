from ud4d.detector import UDevDetector, UEvent, UEventManager


if __name__ == '__main__':
    UDevDetector.start()
    print('udev started')

    for _ in range(16):
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

    UDevDetector.stop()
    print('udev stopped')
