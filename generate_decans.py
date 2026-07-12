import ephem
import math
import datetime
from ics import Calendar, Event

def get_solar_decan(date):
    sun = ephem.Sun()
    sun.compute(date)
    ecl = ephem.Ecliptic(sun)
    lon_deg = math.degrees(ecl.lon)
    
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
             
    # Chaldean order of decan rulers starting from Aries I
    chaldean_cycle = ["Mars", "Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter"]
    
    decan_index = int(lon_deg / 10)
    sign_index = decan_index // 3
    decan_num = (decan_index % 3) + 1
    ruler = chaldean_cycle[decan_index % 7]
    
    return f"Sun in {signs[sign_index]} Decan {decan_num} ({ruler})"

def generate_decans_calendar():
    cal = Calendar()
    today = datetime.datetime.utcnow().date()
    
    prev_decan = get_solar_decan(today)
    block_start_date = today
    
    # 365-day rolling window
    for i in range(1, 365):
        current_date = today + datetime.timedelta(days=i)
        current_decan = get_solar_decan(current_date)
        
        # When the Sun enters a new decan, close the previous block and start a new one
        if current_decan != prev_decan:
            # End date in .ics is exclusive, so the current_date acts as the correct cutoff
            e_block = Event(
                name=prev_decan,
                begin=block_start_date,
                end=current_date
            )
            e_block.make_all_day()
            cal.events.add(e_block)
            
            # Reset for the new block
            prev_decan = current_decan
            block_start_date = current_date
            
    # Close the final block at the end of the year loop
    end_date_exclusive = today + datetime.timedelta(days=366)
    e_block = Event(
        name=prev_decan,
        begin=block_start_date,
        end=end_date_exclusive
    )
    e_block.make_all_day()
    cal.events.add(e_block)
        
    with open("astrological_decans.ics", "w") as f:
        f.writelines(cal.serialize_iter())

if __name__ == "__main__":
    generate_decans_calendar()
