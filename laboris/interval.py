from datetime import datetime


class Interval:

    def __init__(self, start=datetime.now(), end=None):
        if start is None:
            start = datetime.now()
        self.start = start
        self.end = end

    def __repr__(self):
        pass

    def is_done(self):
        if self.end is None:
            return False
        else:
            return True

    def stop(self, date=None):
        if date is None:
            self.end = datetime.now()
        else:
            self.end = date

    def duration(self):
        if self.start is None:
            return 0
        elif self.end is None:
            t = datetime.now() - self.start
            return t.seconds
        else:
            t = self.end - self.start
            return t.seconds

    def parse_json(self, data):
        if len(data) > 0:
            self.start = datetime.fromtimestamp(data[0])
        if len(data) > 1:
            self.end = datetime.fromtimestamp(data[1])

    def get_json(self):
        data = list()
        if self.start is not None:
            data.append(int(self.start.timestamp()))
        if self.end is not None:
            data.append(int(self.end.timestamp()))
        return data

    def print_start(self, sec=False):
        if self.start is None:
            dt = datetime.now()
            if sec is True:
                return dt.strftime("%H:%M:%S")
            elif sec is False:
                return dt.strftime("%H:%M:%S")
            return " - "
        if type(sec) is str:
            return self.start.strftime(sec)
        if sec is True:
            return self.start.strftime("%H:%M:%S")
        elif sec is False:
            return self.start.strftime("%H:%M")

    def print_end(self, sec=False):
        if self.end is None:
            dt = datetime.now()
            if sec is True:
                return dt.strftime("%H:%M:%S")
            elif sec is False:
                return dt.strftime("%H:%M")
            return " - "
        if type(sec) is str:
            return self.end.strftime(sec)
        if sec is True:
            return self.end.strftime("%H:%M:%S")
        elif sec is False:
            return self.end.strftime("%H:%M")

    def get_duration(self):
        if self.start is None:
            return 0
        elif self.end is None:
            return (datetime.now() - self.start).seconds
        else:
            return (self.end - self.start).seconds

    def print_duration(self, sec=False):
        if self.start is None:
            if sec is False:
                return "00:00"
            elif sec is True:
                return "00:00:00"
        elif self.end is None:
            t = datetime.now() - self.start
            second = t.seconds
            minute = int(second / 60)
            second -= (minute * 60)
            hour = int(minute / 60)
            minute -= (hour * 60)
            if sec is False:
                return "{0:02}:{1:02}".format(hour, minute)
            elif sec is True:
                return "{0:02}:{1:02}:{2:02}".format(hour, minute, second)
        else:
            t = self.end - self.start
            second = t.seconds
            minute = int(second / 60)
            second -= (minute * 60)
            hour = int(minute / 60)
            minute -= (hour * 60)
            if sec is False:
                return "{0:02}:{1:02}".format(hour, minute)
            elif sec is True:
                return "{0:02}:{1:02}:{2:02}".format(hour, minute, second)

        return " - "
