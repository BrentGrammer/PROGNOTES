# Cubase

### Moving notes left and right

- click hold and select notes
  - CMD + <- or ->

### Full Screen Mixer

- press F3

## Create MIDI tracks from Instrument Track

- Create an Instrument Track
  - Select Kontakt
  - In Kontakt Player: View > Rack View on
  - Add multiple instruments by dragging from left to the bottom right screen section
  - Assign Channels to each instrument starting at 1 and incrementing (ex: Port A 1)
- Right click on Instrument Track in Cubase > Add Track > Midi Track
  - Leave settings alone (All Midi Tracks and Channel 1 selected)
  - Increment the number of tracks you want and enter a name
- Note: AFter this the Routing section in the inspector does show Any for the midi channel for the first entry, but the channel under the Instrument setting shows the number.

### Outputs

- in Kontakt player > View > Outputs
  - Click Presets / Batch Configuration dropdown
  - Select Batch functions > Clear output selection and create one individual channel for each loaded instrument
  - Alternatively you can manually add channels and then set the output manually on the instrument in Kontakt player
- Set outputs to control the midi tracks individually
- Select Kontakt instrument (not the midi track)
- In left Channel tab, click the right arrow icon at the top and select outputs
  - i.e. select KT {instrument name}
  - these will be added to your mixer and represent each midi track so you can control volume and mix etc.

## Optimizing RAM
- Purge samples (i.e. in Kontakt)
- Load instruments into a Rack instrument. See [vid](https://www.udemy.com/course/cubase-complete-course/learn/lecture/34818318#notes)
- Can create individual instrument tracks, but you need to disable them to save ram.
