# calendar-to-hue
Connector to enable triggering of Philips Hue bulbs from Google Calendar events

## Setup

### Setup Hue Account
1. Set up a [Hue developer account](https://developers.meethue.com)
2. Create an app in the [Hue developer portal](https://developers.meethue.com/my-apps/)
3. If this is just local and for testing - Callback URL can be set to `http://127.0.0.1/`
4. A `ClientId` and `ClientSecret` will be generated for you

### Get the local IP Address of your 
1. This app will attempt to automatically get the local IP address of your Hue Bridge.
2. If you have multiple Hue Bridges or the app struggles to get your address, then you can set it manually in xxxxx. There are [guides](https://developers.meethue.com/develop/application-design-guidance/hue-bridge-discovery/) or [this link](https://discovery.meethue.com/) might show it.

## To-do 
- Need to add code for authorising API, if success - store key 
- Create a DB to store scheduled events
- Set up react front end to make UI more interactive:
- - Make the current time refresh
- - Listen for trigger events and update the UI when they trigger
- - List for gcalendar changes
Make the refresh button run individual changes:
- 
