# Christina LaPane Student ID: 008207171

# this class is to take strings of time and make it into the format HH:mm AM/PM
class Time(object):
    def __init__(self, *args):
        super().__init__()

        # splits the string into hours and minutes and AM/PM
        if len(args) == 1:
            time_str = args[0]
            time_str_parts = time_str.split(':')
            hours = float(time_str_parts[0].strip())
            time_str_parts = time_str_parts[1].split(' ')
            minutes = float(time_str_parts[0].strip())
            ap = time_str_parts[1].strip()
            if ap.upper() == 'AM':   # if AM then 0 - 12 transforms into 12AM -11 AM
                if hours == 12:
                    self.hours = 0
                else:
                    self.hours = hours
                self.minutes = minutes
            else:                       # if PM, then 13 - 23 transforms into 12PM - 11PM
                self.hours = hours + 12
                self.minutes = minutes
        elif len(args) == 2:
            self.hours = args[0]
            self.minutes = args[1]
        else:
            print('Unsupported')

    def add_minutes(self, minutes):
        combined_minutes = self.minutes + minutes
        if combined_minutes >= 60:               # if minutes are greater than 60
            hours = (combined_minutes // 60)    # then total minutes divided by 60, rounded down. Ex: 59.43 == 59 Minutes
            self.hours += hours
            combined_minutes = (combined_minutes - (hours * 60))
        self.minutes = combined_minutes

    # returns horus and minutes entereed into correct format
    def __eq__(self, value):
        return self.hours == value.hours and self.minutes == value.minutes

    def __ne__(self, value):
        return not self.__eq__(value)

    def __lt__(self, value):
        if self.hours < value.hours:
            return True
        elif self.hours > value.hours:
            return False
        else:
            if self.minutes < value.minutes:
                return True
            else:
                return False

    def __le__(self, value):
        if self.hours < value.hours:
            return True
        elif self.hours > value.hours:
            return False
        else:
            if self.minutes <= value.minutes:
                return True
            else:
                return False

    def __gt__(self, value):
        if self.hours > value.hours:
            return True
        elif self.hours < value.hours:
            return False
        else:
            if self.minutes > value.minutes:
                return True
            else:
                return False

    def __ge__(self, value):
        if self.hours > value.hours:
            return True
        elif self.hours < value.hours:
            return False
        else:
            if self.minutes >= value.minutes:
                return True
            else:
                return False

    # determines if should be AM or PM based off 0 - 12, or 13 - 24
    def __str__(self):
        ap = None
        if self.hours < 12:
            ap = 'AM'
        else:
            ap = 'PM'
        adjusted_hours = (self.hours % 12)
        if adjusted_hours == 0:
            adjusted_hours += 12
        return '{:02d}:{:02d} {}'.format(int(adjusted_hours), int(self.minutes), ap)