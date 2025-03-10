import requests

base_url = "http://localhost:4001"


def create_gig(venue_id, client_id, date, time):
    response = requests.post(
        f"{base_url}/api/gigs",
        json={
            "venue_id": venue_id,
            "client_id": client_id,
            "date": date,
            "time": time,
        },
    )
    print(f"Created gig: {response.json()}")
    return response.json()


# second gig close to the notification window
time1 = "12:00"
date = "2026-01-01"
venue = "First Venue"
gig1 = create_gig(venue, date, time1)
time2 = "18:00"
venue = "Second Venue"
gig2 = create_gig(venue, date, time2)

# Second gig in the notification window (but before)
time3 = "11:00"
venue = "Third Venue"
gig3 = create_gig(venue, date, time3)

# Second gig in the notification window (but after)
time4 = "19:00"
venue = "Fourth Venue"
gig4 = create_gig(venue, date, time4)

# Second gig at the same time as another
venue = "Fifth Venue"
gig5 = create_gig(venue, date, time4)

# Gig bewtween to gigs that should both notify
time5 = "14:00"
venue = "Sixth Venue"
gig6 = create_gig(venue, date, time5)
