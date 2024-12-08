from datetime import datetime, timedelta

class time_handler():
  def __init__(self):
    # starting at May 1st cause thats when summer starts
    self.current_date = datetime(2024, 5, 1)
  
  def get_season(self):
    year = self.current_date.year
    summer = {
      "start": datetime(year, 5, 1),
      "end": datetime(year, 10, 31)
    }
    winter = {
      "start": datetime(year, 11, 1),
      "end": datetime(year+1, 4, 30)
    }
    if summer["start"]<=self.current_date<summer["end"]:
      return "summer"
    else:
      return "winter"
  
  def is_weekend(self):
    if self.current_date.weekday()<5:
      return False
    return True
  
  def end_day(self):
    self.current_date += timedelta(days=1)
