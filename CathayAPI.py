import requests
import json

print("please state your type of request")
print("requests available: bag allowance, customer details, regulatory requirement, seat map and flight details")
requested = input()

print("please state your booking ID")
bookingID = input() #6I4CKI

if len(bookingID) != 6:
    print("invalid booking ID")
elif "bag" in requested or "allowance" in requested:
    url = f"https://developers.cathaypacific.com/hackathon-apigw/hackathon-middleware/v1/airport/customers/{bookingID}/bagallowance"
elif "customer details" in requested:
    url = f"https://developers.cathaypacific.com/hackathon-apigw/hackathon-middleware/v1/airport/customers/{bookingID}/details"
elif "regulatory" in requested or "requirement" in requested:
    url = f"https://developers.cathaypacific.com/hackathon-apigw/hackathon-middleware/v1/airport/customers/{bookingID}/regulatoryrequirements"
elif "seat" in requested or "map" in requested:
    url = f"https://developers.cathaypacific.com/hackathon-apigw/hackathon-middleware/v1/airport/flights/{bookingID}/seatmaps"
elif "flight details" in requested:
    url = f"https://developers.cathaypacific.com/hackathon-apigw/hackathon-middleware/v1/airport/flights/{bookingID}"
else:
    print("Function not yet developed")


payload = {}
headers = {
  'apiKey': '0Ws2MAmAseTl39JZLohswZZgWLCxpZ1K'
}

responses = requests.request("GET", url, headers=headers, data=payload)


if "bag" in requested or "allowance" in requested:

    try:
        response = json.loads(responses.text)
        data = response["data"][0]
    except KeyError:
        print("Booking not found")
    
    is_pooled_allowance = data["isPooledAllowance"]
    passenger_id = data["dcsPassengers"][0]["id"]
    departure_code = data["segmentDeliveries"][0]["flightSegment"]["departure"]["iataCode"]
    arrival_code = data["segmentDeliveries"][0]["flightSegment"]["arrival"]["iataCode"]
    total_allowance = data["baggageGroupAllowances"]["baggageGroupAllowance"]["quantity"]
    adult_allowance = data["baggageGroupAllowances"]["baggageAllowanceBreakdowns"][0]["quantity"]
    weight_per_piece = data["baggageGroupAllowances"]["baggageAllowanceBreakdowns"][1]["weight"]["amount"]
    weight_unit = data["baggageGroupAllowances"]["baggageAllowanceBreakdowns"][1]["weight"]["unit"]

    readable_text = f"""
Baggage Information:
- Passenger ID: {passenger_id}
- Departure: {departure_code}
- Arrival: {arrival_code}
- Total Baggage Allowance: {total_allowance} (TOTAL_ALLOWANCE)
- Adult Allowance: {adult_allowance} piece(s) (ADULT_ALLOWANCE)
- Weight per Piece: {weight_per_piece} {weight_unit} (WEIGHT_PER_PIECE)
"""
    print(readable_text)

elif "customer details" in requested:
    try:    
        data = json.loads(responses.text)
        passenger_info = data['data']['traveler']
        first_name = passenger_info['name']['firstName']
        last_name = passenger_info['name']['lastName']
        gender = passenger_info['gender']
        passenger_type = passenger_info['passengerTypeCode']
        flight_info = data['dictionaries']['datedFlight']['CX238120241107PVG']
        departure_info = flight_info['flightPoints'][0]
        arrival_info = flight_info['flightPoints'][1]
        departure_time = departure_info['departure']['timings'][0]['value'] if 'timings' in departure_info['departure'] else 'N/A'
        arrival_time = arrival_info['timings'][0]['value'] if 'timings' in arrival_info else 'N/A'
        departure_iata = departure_info['iataCode']
        arrival_iata = arrival_info['iataCode']

        included_data = data.get('included', {})
    except KeyError:
        print("Booking not found")
    
    if 'segmentDeliveries' in included_data:
        segment_deliveries = included_data['segmentDeliveries']
        flight_segment = segment_deliveries['5007F415000272FF']['flightSegment']
        flight_number = flight_segment['operating']['number']
        departure_terminal = flight_segment['departure']['terminal']
        arrival_terminal = flight_segment['arrival']['iataCode']

        print("\n=== Flight Information ===")
        print(f"Flight Number: CX{flight_number}")
        print(f"Departure Airport: {departure_iata}")
        print(f"Departure Terminal: {departure_terminal}")
        print(f"Scheduled Departure: {departure_time}")
        print(f"Arrival Airport: {arrival_iata}")
        print(f"Arrival Terminal: {arrival_terminal}")
        print(f"Scheduled Arrival: {arrival_time}")
        
        
        
    else:
        print("No data found.")

    print("\n=== Passenger Information ===")
    print(f"Name: {first_name} {last_name}")
    print(f"Gender: {gender}")
    print(f"Passenger Type: {passenger_type}")



   
elif "regulatory" in requested or "requirement" in requested:
    data = json.loads(responses.text)
    try:
        segment_deliveries = data['data'][0].get('segmentDeliveries', [])
    except KeyError:
        print("No booking found")
    if segment_deliveries:
        print("\n=== Segment Deliveries ===")
        for segment in segment_deliveries:
            segment_id = segment.get('id', 'N/A')
            segment_ref = segment.get('ref', 'N/A')
            print(f"Segment ID: {segment_id}")
            print(f"Reference: {segment_ref}")
    else:
        print("No segment deliveries found.")
    warnings = data.get('warnings', [])
    if warnings:
        print("\n=== Warnings ===")
        for warning in warnings:
            print(f"Code: {warning['code']}")
            print(f"Title: {warning['title']}")
            print(f"Detail: {warning['detail']}")
            print(f"Pointer: {warning['pointer']}")
    else:
        print("No warnings found.")
    regulatory_checks = data['included']['segmentDeliveries']['5007F415000272FF']['legDeliveries'][0].get('regulatoryChecks', [])
    if regulatory_checks:
        print("\n===Regulatory Checks===")
        for check in regulatory_checks:
            check_id = check.get('id', 'N/A')
            check_ref = check.get('ref', 'N/A')
            print(f"Check ID: {check_id}")
            print(f"Check Reference: {check_ref}")
    else:
        print("No regulatory checks found.")

    regulatory_requirements = data['dictionaries']['regulatoryRequirements']
    if regulatory_requirements:
        print("\n=== Regulatory Requirements Status ===")
        for requirement_id, requirement in regulatory_requirements.items():
            program_name = requirement['regulatoryProgram']['name']
            is_successful = requirement['isOverallSuccess']
            print(f"Program: {program_name}")
            print(f"Status: {'Success' if is_successful else 'Not Performed'}")
            for status in requirement['statuses']:
                print(f"  Status Code: {status['statusCode']}")
                print(f"  Description: {status.get('humanReadableDescription', 'N/A')}")
    else:
        print("No regulatory requirements found.")
elif "seat" in requested or "map" in requested:
    try:
        data = json.loads(responses.text)
        seatmap = data['data']['seatmaps'][0]
        leg = seatmap["leg"]
    except KeyError:
        print("No booking found")

    flight_info = {
        "Boarding Point": leg["boardPointIataCode"],
        "Offboarding Point": leg["offPointIataCode"],
        "Aircraft Type": leg["aircraftEquipment"]["aircraftType"],
        #"Cabin Configuration": leg["aircraftEquipment"]["aircraftConfiguration"]
    }

    print("Flight Information:")
    print(f"Boarding Point (IATA Code): {flight_info['Boarding Point']}")
    print(f"Offboarding Point (IATA Code): {flight_info['Offboarding Point']}")
    print(f"Aircraft Type: {flight_info['Aircraft Type']}")
    #print(f"Cabin Configuration: {flight_info['Cabin Configuration']}")
    seat_number = input("Enter the seat number: ") 
    seats_found = []
    row_number = None

    for cabin in seatmap["cabinDetails"]:
        for seat in cabin.get("seats", []):
            if seat["number"] == seat_number:
                row_number = seat["row"] 
                break

    if row_number is not None:
        for cabin in seatmap["cabinDetails"]:
            for seat in cabin.get("seats", []):
                if seat["row"] == row_number:
                    for pricing in seat.get("travelerPricing", []):
                        seat_info = {
                            "Seat Number": seat["number"],
                            "Availability": pricing["seatAvailabilityStatus"],
                            "Price": f"{pricing['price']['sellingTotal']} {pricing['price']['currency']}",
                            "Row": seat["row"],
                            "Column": seat["column"],
                            "Zone": seat["zone"],
                        }
                        seats_found.append(seat_info)

        # Displaying seating details for all seats in the same row
        if seats_found:
            print(f"\nSeating details for row number: {row_number}")
            for seat in seats_found:
                print(f"\nSeat Number: {seat['Seat Number']}")
                print(f"Row: {seat['Row']}, Column: {seat['Column']}")
                print(f"Availability: {seat['Availability']}")
                print(f"Price: {seat['Price']}")
                
    else:
        print("No seating information found for this seat number.")
elif "flight details" in requested:
    try:
        data = json.loads(responses.text)
        flight_id = data["data"]["id"]
        departure_date = data["data"]["scheduledDepartureDate"]
        carrier = data["data"]["flightDesignator"]["carrierCode"]
        flight_number = data["data"]["flightDesignator"]["flightNumber"]
    except KeyError:
        print("No bookings found")
    
    print("=== Flight Information ===")
    print(f"Flight ID: {flight_id}")
    print(f"Scheduled Departure Date: {departure_date}")
    print(f"Carrier: {carrier}")
    print(f"Flight Number: {flight_number}")
    print("\n")

    for flight_point in data["data"]["flightPoints"]:
        iata_code = flight_point["iataCode"]
        departure_terminal = flight_point["departure"]["terminal"]["code"]
        if "arrival" in flight_point and "terminal" in flight_point["arrival"] and "code" in flight_point["arrival"]["terminal"]:
            arrival_terminal = flight_point["arrival"]["terminal"]["code"]
        else:
            pass
        
        if "departure" in flight_point and "timings" in flight_point["departure"]:
            departure_timings = flight_point["departure"]["timings"]
        else:
            pass
        for timing in departure_timings:
            if timing["qualifier"] == "STD":
                departure_time = timing["value"]
                print(f"Departure from {iata_code} (Terminal {departure_terminal}): {departure_time}")
        
        if "arrival" in flight_point and "timings" in flight_point["arrival"]:
            arrival_timings = flight_point["arrival"]["timings"]
        else:
            pass
        for timing in arrival_timings:
            if timing["qualifier"] == "STA":
                arrival_time = timing["value"]
                print(f"Arrival at {iata_code} (Terminal {arrival_terminal}): {arrival_time}")
                
        
        print("\n")


    print("=== Boarding Information ===")
    for leg in data["included"]["legs"]:
        board_point = leg["boardPointIataCode"]
        off_point = leg["offPointIataCode"]
        flying_time = leg["flyingTimeDuration"]
        aircraft_type = leg["aircraftEquipment"]["aircraftType"]
        aircraft_config = leg["aircraftEquipment"]["aircraftConfiguration"]["code"]
        
        print(f"Board Point: {board_point}")
        print(f"Off Point: {off_point}")
        print(f"Flying Time: {flying_time}")
        print(f"Aircraft Type: {aircraft_type}")
        print(f"Aircraft Configuration: {aircraft_config}")
        
        print("\n")

    print("=== Cabin Information ===")
    for leg in data["included"]["legs"]:
        for cabin in leg["legCounters"]["cabinCounters"]:
            cabin_name = cabin["cabinName"]
            capacity = cabin["counters"]["capacity"]
            availability = cabin["counters"]["availability"]
            booked = cabin["counters"]["booked"]
            accepted = cabin["counters"]["accepted"]
            
            print(f"Cabin: {cabin_name}")
            print(f"Capacity: {capacity}")
            print(f"Availability: {availability}")
            print(f"Booked: {booked}")
            print(f"Accepted: {accepted}")
            print("\n")













