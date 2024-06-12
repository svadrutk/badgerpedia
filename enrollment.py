import requests
import json
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import traceback
from datetime import datetime, timedelta
import time


# you can also import SoftwareEngine, HardwareType, SoftwareType, Popularity from random_user_agent.params
# you can also set number of user agents required by providing `limit` as parameter

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

# Get list of user agents.
user_agents = user_agent_rotator.get_user_agents()



def get_current_class_terms():
  currYear = time.localtime().tm_year
  possibleCodes = [1014 + (currYear - 2001) * 10, 1016 + (currYear - 2001) * 10, 1022 + (currYear - 2001) * 10]
  # check what month it is
  currMonth = time.localtime().tm_mon
  if currMonth >= 5 and currMonth < 9:
    return possibleCodes[2]
  elif currMonth > 9:
    return possibleCodes[0]
  else:
    return possibleCodes[1]


# Get Random User Agent String.
def get_class_codes(name):
  term = get_current_class_terms()
  try:
    user_agent = user_agent_rotator.get_random_user_agent()

    url = "https://public.enroll.wisc.edu/api/search/v1"
    course_name = name
    if '/' in course_name:
      course_name = course_name.split('/')[1]

    def get_referrer():
      base = f"https://public.enroll.wisc.edu/search?term={term}&keywords="
      end = ""
      course_name_split = course_name.split(" ")

      index = 0
      for c in course_name_split:
        if(index == (len(course_name_split) - 1)):
          end += c
        else:
          end += (c + "%20")

        index += 1
      print(base + end)
      return (base + end + "&closed=true")


    payload = json.dumps({
    "selectedTerm": term,
    "queryString": course_name,
    "page": 1,
    "pageSize": 1,  # Set this to the maximum allowed value by the API
    "sortOrder": "SCORE"
    })
    headers = {
      'Accept': 'application/json, text/plain, */*',
      'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
      'Connection': 'keep-alive',
      'Content-Type': 'application/json',
      'Cookie': 'uw_madison_cookieconsent_timestamp=1667888356; uw_madison_cookieconsent_url=https://gened.wisc.edu/; _clck=q1b669|1|f6h|0; _ga_PKMD7J9C1Y=GS1.1.1668208955.1.0.1668208955.0.0.0; _hjSessionUser_14571=eyJpZCI6IjkxOTg0YzgwLTczYTctNTEwMi04NzUzLWI5MmYyNWQ3ZWEwOCIsImNyZWF0ZWQiOjE2Njc1MjAxMzE0MDcsImV4aXN0aW5nIjp0cnVlfQ==; _ga_H8TY6JPKPY=GS1.1.1669051960.1.1.1669052039.0.0.0; _hjSessionUser_454181=eyJpZCI6IjVmM2MzY2FmLWE5NWYtNWI0OC1hY2NhLTQwY2E2ZjY0YzM3NyIsImNyZWF0ZWQiOjE2Njk2NTUwNzYwOTQsImV4aXN0aW5nIjp0cnVlfQ==; _ga_1KZJ965FVN=GS1.1.1674479503.1.0.1674479520.0.0.0; _ga_HB1DSNSVZS=GS1.1.1674673671.3.0.1674673674.0.0.0; _ga_8N0WSPV9ZS=GS1.1.1676056105.6.0.1676056110.0.0.0; _hjSessionUser_15573=eyJpZCI6ImE1MDJmMzBiLTk4ODEtNWFmOC1hNzA3LTc4N2MyNWIwMTU3MiIsImNyZWF0ZWQiOjE2NzYyNjg2MjcxOTEsImV4aXN0aW5nIjp0cnVlfQ==; _ga_D04HXCEERG=GS1.1.1676830452.4.1.1676830472.0.0.0; _ga_MSP0G8LW4X=GS1.1.1677187991.5.0.1677187999.0.0.0; _ga_0P124BMQ7M=GS1.1.1677528453.2.1.1677529904.0.0.0; _ga_BR24HS4WL2=GS1.1.1677564211.4.0.1677564211.0.0.0; _ga_DRHZVXYET9=GS1.1.1679953218.2.0.1679953218.0.0.0; _ga_SD6W5B6HXB=GS1.1.1680625429.1.1.1680626494.0.0.0; _ga_WDL7EFFME9=GS1.1.1680624437.1.1.1680626511.0.0.0; _ga_28VQH1JQ71=GS1.1.1681081032.2.1.1681081486.0.0.0; tracking_ga=GA1.1.870007653.1681081593; tracking_ga_2SJ4PP2F5X=GS1.1.1681081592.1.0.1681081595.0.0.0; _ga_JPYYW8RQW6=GS1.1.1681430509.5.0.1681430509.0.0.0; _ga_PL4XLHJ3ZV=GS1.1.1681493863.2.0.1681493866.0.0.0; _ga_SQBP9T2Z82=GS1.1.1681657900.2.0.1681657901.59.0.0; _ga_RVG8ZSR4RJ=GS1.1.1681846908.2.0.1681846912.0.0.0; _gcl_au=1.1.1944106783.1681860325; nmstat=616f57ff-9b75-afe6-5424-1b969092ac64; _ga_EHCSFMPLK0=GS1.1.1681860325.1.0.1681860328.57.0.0; ELOQUA=GUID=4969DD37BC064D47B3FB2D81DA4664AE; ELQSTATUS=OK; _ga_CLJPG4TYB9=GS1.1.1682273495.4.1.1682273524.31.0.0; _ga_GNQ7QL8EWJ=GS1.1.1682962318.12.0.1682962318.0.0.0; _ga_D48GGC808B=GS1.1.1683413393.16.0.1683413393.0.0.0; _hp2_id.3001039959=%7B%22userId%22%3A%227557292187725567%22%2C%22pageviewId%22%3A%226601487835979906%22%2C%22sessionId%22%3A%221107558558734040%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _hjSessionUser_1084037=eyJpZCI6IjdlOGE1NTBiLTlmZWEtNTU2YS04MDZhLTBlZGJiN2ZiNDMxMiIsImNyZWF0ZWQiOjE2ODA2Mjc2Mzg2MzYsImV4aXN0aW5nIjp0cnVlfQ==; _ga_W0LVWV6QC1=GS1.1.1685870414.7.0.1685870414.0.0.0; _ga_97T62X0QM2=GS1.1.1685870414.74.0.1685870421.0.0.0; _ga_492DKHNP76=GS1.1.1685870459.6.0.1685871090.0.0.0; _ga_JZF3EQ0J3C=GS1.1.1685882444.1.1.1685882484.0.0.0; _ga_9NRE1T4SDT=GS1.1.1685882444.1.1.1685882484.0.0.0; _ga_PLJ9E3ZY82=GS1.1.1685882494.13.1.1685882510.0.0.0; _gid=GA1.2.1872109422.1686283491; _ga_NWHT10P6DB=GS1.1.1686417573.6.1.1686417731.0.0.0; _gat=1; _ga_BMXBQNSW2Q=GS1.1.1686453609.3.1.1686453644.0.0.0; _ga=GA1.1.819226642.1683701179; AWSALB=J2jaUVVA2FhMt1DwAndNYMo6rYIUEWbe16d3bwG5CCnO2tK1j214CXOjyjt0c05N7nL5nDgMD/x8ZPqIEvf3hY5qaFCrq+8xELk03IlgIxXahuqOeRSCrPC6NuVb; AWSALBCORS=J2jaUVVA2FhMt1DwAndNYMo6rYIUEWbe16d3bwG5CCnO2tK1j214CXOjyjt0c05N7nL5nDgMD/x8ZPqIEvf3hY5qaFCrq+8xELk03IlgIxXahuqOeRSCrPC6NuVb; AWSALB=4KJwQ3qOSWYG/vgtw3pMWb8dRZNMt4ukQv1lIrjKTKa5lIS7MCkey3lRUwOcXgeTMpTYMvtKHe6jeZr6fPMd4LhGxnYclmRutIAefDPuykNsivHzruy9fklGQxQT; AWSALBCORS=4KJwQ3qOSWYG/vgtw3pMWb8dRZNMt4ukQv1lIrjKTKa5lIS7MCkey3lRUwOcXgeTMpTYMvtKHe6jeZr6fPMd4LhGxnYclmRutIAefDPuykNsivHzruy9fklGQxQT',
      'Origin': 'https://public.enroll.wisc.edu',
      'Referer': get_referrer(),
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'User-Agent': user_agent,
      'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"macOS"'
    }

    # proxies = {
    #   "http": "http://gate2.proxyfuel.com:2000",
    #   "https": "http://gate2.proxyfuel.com:2000"
    #  }

    # print("Sending request for " + name + "...")
    # response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)

    print("Sending request for " + name + "...")
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    print("Response found!")
    responseDict = response.json()
    courseCode = responseDict['hits'][0]['subject']['subjectCode']
    subjectCode = responseDict['hits'][0]['courseId']
    return [subjectCode, courseCode]


  except Exception:
    print(traceback.print_exc())
    return [False, name]


def get_enrollment(class_codes):
  print(class_codes)
  term = get_current_class_terms()
  subjectCode = class_codes[1]
  courseCode = class_codes[0]

  try:
    user_agent = user_agent_rotator.get_random_user_agent()

    url = "https://public.enroll.wisc.edu/api/search/v1/enrollmentPackages/" + str(term) + "/" + str(subjectCode) + "/" + str(courseCode)

    print(url)
    response = requests.get(url, headers={'User-Agent': user_agent})
    response = response.json()
    classData = response
    return classData
  except Exception:
    print(traceback.print_exc())
    return False

def get_capacity(data):
    # Access the enrollmentStatus object
    capacity = 0
    currently_enrolled = 0

    if(len(data) == 0) or (data == None):
      return [0, 1]

    for i in range(len(data)):
      enrollment_status = data[i]['enrollmentStatus']
      if(enrollment_status['aggregateCapacity'] == None):
        capacity += enrollment_status['capacity']
      else:
        capacity += enrollment_status['aggregateCapacity']

      if(enrollment_status['aggregateCurrentlyEnrolled'] == None):
        currently_enrolled += enrollment_status['currentlyEnrolled']
      else:
        currently_enrolled += enrollment_status['aggregateCurrentlyEnrolled']
    return [currently_enrolled, capacity]


def custom_sort(item):
  # Primary sort key: lecNum (as integer for numerical sorting)
    lec_num = int(item['lecNum'])

    # Secondary sort key: 'type' with 'LEC' being considered smaller than others
    type_order = 0 if item['type'] == 'LEC' else 1

    # Tertiary sort key: sectionNumber as integer (descending order)
    section_num = int(item['sectionNumber'])

    # Sorting by lecNum ascending, type_order ascending, sectionNumber descending
    return (lec_num, type_order, section_num)

def extract_class_info(json_data):
    if len(json_data) == 0:
        empty = [{
            "type": "N/A",
            "sectionNumber": "N/A",
            "lecNum": "N/A",
            "instructor": "N/A",
            "meetingDays": "N/A",
            "meetingTimes": ["N/A", "N/A"],
            "location": ["N/A", "N/A"],
            "currentlyEnrolled": 0,
            "capacity": 1,
            "waitlistCurrentSize": 0
        }]
        return empty

    class_info_list = []

    for class_data in json_data:
        sections = class_data.get("sections", [])
        lecNum = class_data.get('autoEnrollClasses', [class_data['id']])[0]

        for section in sections:
            typ = section.get("type", "N/A")
            secNum = section.get("sectionNumber", "N/A")
            meeting_info_list = section.get("classMeetings", [{}])
            if meeting_info_list:  # Check if the list is not empty
                meeting_info = meeting_info_list[0]  # Access the first element
            else:
                meeting_info = {}  # Assign an empty dictionary as default value
            enrollment_status = section.get("enrollmentStatus", {})

            instructor = "TBA"
            if section.get('instructor') and section['instructor'].get('name'):
                instructor = f"{section['instructor']['name'].get('first', 'TBA')} {section['instructor']['name'].get('last', 'TBA')}"

            startTime = ms_to_time(meeting_info.get("meetingTimeStart", "N/A"))
            endTime = ms_to_time(meeting_info.get("meetingTimeEnd", "N/A"))

            meetingDaysList = meeting_info.get("meetingDaysList", [])
            if not meetingDaysList:
                meetingDaysList = [section.get("classMeetings", [{}])[i].get("meetingDays", []) for i in range(len(section.get("classMeetings", [])))]
                meetingDaysList = [day for sublist in meetingDaysList if sublist for day in sublist]  # Flatten list and handle None values

            building = "N/A"
            room = "N/A"
            if meeting_info == None:
                building = "N/A"
                room = "N/A"
            else:
                building = meeting_info.get("building", {})
                if building != None:
                  building = building.get("buildingName", "N/A")
                else:
                  building = "N/A"
                room = meeting_info.get("room", "N/A")

            currentlyEnrolled = enrollment_status.get("currentlyEnrolled")
            aggregateCurrentlyEnrolled = enrollment_status.get("aggregateCurrentlyEnrolled")

            if currentlyEnrolled is None and aggregateCurrentlyEnrolled is None:
                currentlyEnrolled = "N/A"
            else:
                currentlyEnrolled = max(
                    currentlyEnrolled if currentlyEnrolled is not None else 0,
                    aggregateCurrentlyEnrolled if aggregateCurrentlyEnrolled is not None else 0
                )

            capacity = enrollment_status.get("capacity")
            aggregateCapacity = enrollment_status.get("aggregateCapacity")

            if capacity is None and aggregateCapacity is None:
                capacity = "N/A"
            else:
                capacity = max(
                    capacity if capacity is not None else 1,
                    aggregateCapacity if aggregateCapacity is not None else 1
                )


            waitlistCurrentSize = enrollment_status.get("waitlistCurrentSize", 0)

            currentlyEnrolled = currentlyEnrolled if currentlyEnrolled is not None else 0
            capacity = capacity if capacity is not None else 1
            waitlistCurrentSize = waitlistCurrentSize if waitlistCurrentSize is not None else 0

            class_info = {
                "type": typ,
                "sectionNumber": secNum,
                "lecNum": lecNum,
                "instructor": instructor,
                "meetingDays": meetingDaysList,
                "meetingTimes": [startTime, endTime],
                "location": [room, building],
                "currentlyEnrolled": int(currentlyEnrolled),
                "capacity": int(capacity),
                "waitlistCurrentSize": int(waitlistCurrentSize),
            }
            class_info_list.append(class_info)

    for d in class_info_list:
        dayList = []
        days = d['meetingDays']
        for day in days:
            if day in ['MONDAY', 'M']:
                dayList.append('M')
            elif day in ['TUESDAY', 'T']:
                dayList.append('T')
            elif day in ['WEDNESDAY', 'W']:
                dayList.append('W')
            elif day in ['THURSDAY', 'R']:
                dayList.append('R')
            elif day in ['FRIDAY', 'F']:
                dayList.append('F')
        d['meetingDays'] = ''.join(dayList)

    sorted_data = sorted(class_info_list, key=custom_sort)
    seen = set()
    unique_sorted_data = []

    for d in sorted_data:
        d_tuple = (d['type'], d['sectionNumber'])
        if d_tuple not in seen:
            unique_sorted_data.append(d)
            seen.add(d_tuple)

    return unique_sorted_data

def ms_to_time(milliseconds):
    if milliseconds == "N/A":
        return "N/A"
    seconds = milliseconds // 1000
    minutes = (seconds // 60) % 60
    hours = (seconds // 3600) % 24
    return f"{hours:02}:{minutes:02}"


def ms_to_time(ms):
  if ms is None:
    return None
  if ms == "N/A":
    return "N/A"
  sixpm = datetime.strptime("18:00", "%H:%M")
  tm = sixpm + timedelta(milliseconds=ms)
  return tm.strftime("%I:%M %p")


# jsonData = get_enrollment(get_class_codes("L I S 461"))
# print(extract_class_info(jsonData))
