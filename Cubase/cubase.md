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

### MIDI Channels vs. Output Channels:

#### MIDI Channels (e.g., Ch. 1, Ch. 2):

- What They Do: MIDI channels tell Kontakt which instrument to play when you send MIDI data from Cubase. They’re like a remote control for triggering sounds.
- Where You Set Them: In Kontakt, you assign each instrument a MIDI channel (e.g., Violins on Ch. 1, Violas on Ch. 2) in the instrument header. In Cubase, you match this by setting your MIDI track’s channel to Ch. 1 for Violins, Ch. 2 for Violas, etc.
- Purpose: MIDI channels handle input—they decide which instrument responds to your notes or keyswitches.

#### Audio Channels (e.g., [3+4] in St. 2):

- What They Do: These are the output paths Kontakt uses to send the audio from each instrument to Cubase. Think of them as pipes carrying the sound after it’s triggered.
- Where You Set Them: In Kontakt’s Outputs panel, you define stereo pairs like St. 2 [3+4], St. 3 [5+6], etc., and assign instruments to them. Cubase then sees these as separate mixer channels.
- Purpose: Audio channels handle output—they determine where the sound goes for mixing (e.g., Violins to one mixer channel, Violas to another).

### Outputs

NOTE: You may need to restart Cubase if you do not see the new instrument created in the list!

- in Kontakt player > View > Outputs
  - Click Presets / Batch Configuration dropdown
  - Select Batch functions > Clear output selection and create one individual channel for each loaded instrument
  - Alternatively you can manually add channels and then set the output manually on the instrument in Kontakt player
- Set outputs to control the midi tracks individually
- Select Kontakt instrument (not the midi track)
- In left Channel tab, click the right arrow icon at the top and select outputs
  - i.e. select KT {instrument name}
  - these will be added to your mixer and represent each midi track so you can control volume and mix etc.

## Assigning Audio Outputs in Kontakt with Cubase for an Orchestral Setup

### 1. Add Kontakt in Cubase

- Press `F11` (Studio > VST Instruments).
- Click `+`, select **Kontakt 7 (16out)** (or 64out for larger setups).
- Name it “Orchestra” in the rack.

### 2. Load Instruments in Kontakt

- Load instruments with articulations into slots:
  - Slots 1–4: Strings (e.g., Violins Sustain Ch. 1, Violins Staccato Ch. 1, Violas Sustain Ch. 2, Violas Staccato Ch. 2)
  - Slots 5–7: Brass (e.g., Trumpets Sustain Ch. 3, Trumpets Staccato Ch. 3, Horns Sustain Ch. 4)
  - Slots 8–10: Woodwinds (e.g., Flutes Sustain Ch. 5, Oboes Staccato Ch. 6, Clarinets Sustain Ch. 7)
  - Slots 11–13: Percussion (e.g., Timpani Ch. 8, Snares Ch. 9, Cymbals Ch. 10)
- Use same MIDI channel for articulations within a section (e.g., all Violins on Ch. 1), different channels between sections.

### 3. Configure Outputs in Kontakt

- Click **Workspace** icon > **Outputs**.
- In Outputs panel:
  - Click `+`.
  - Set **Quantity:** Number of unique outputs needed (e.g., 10 for Violins, Violas, Trumpets, Horns, Flutes, Oboes, Clarinets, Timpani, Snares, Cymbals).
  - Set **Channels:** 2 (stereo).
  - Assign outputs starting from St. 2:
    - St. 2 [3+4] (Violins)
    - St. 3 [5+6] (Violas)
    - St. 4 [7+8] (Trumpets)
    - St. 5 [9+10] (Horns)
    - St. 6 [11+12] (Flutes)
    - St. 7 [13+14] (Oboes)
    - St. 8 [15+16] (Clarinets)
    - St. 9 [17+18] (Timpani)
    - St. 10 [19+20] (Snares)
    - St. 11 [21+22] (Cymbals)
  - Check **Ascending output assignment**.
  - Click **OK**.
- Assign outputs in Kontakt:
  - Each instrument to its own output (e.g., Violins Sustain > St. 2, Violas Staccato > St. 3).

### 4. Set Up Grouped MIDI Tracks in Cubase

- Add Folder: Project > Add Track > Folder, name it “Orchestra Folder”.
- Add MIDI Tracks (in folder) per section and articulation:
  - “Violins Sustain” (Output: Orchestra, Ch. 1)
  - “Violins Staccato” (Output: Orchestra, Ch. 1)
  - “Violas Sustain” (Output: Orchestra, Ch. 2)
  - “Trumpets Sustain” (Output: Orchestra, Ch. 3)
  - “Horns Staccato” (Output: Orchestra, Ch. 4)
  - “Flutes Sustain” (Output: Orchestra, Ch. 5)
  - (Continue for all sections/articulations)

### 5. Activate Outputs in Cubase

- Press `F11`, click arrow next to “Orchestra”.
- Select **Activate Outputs**.
- Check outputs used (e.g.):
  - Kt. St. 2 [Stereo] (Violins)
  - Kt. St. 3 [Stereo] (Violas)
  - Kt. St. 4 [Stereo] (Trumpets)
  - Kt. St. 5 [Stereo] (Horns)
  - Kt. St. 6 [Stereo] (Flutes)
  - (Up to St. 11 or more)

### 6. Verify in MixConsole

- Press `F3` (MixConsole).
- Rename channels to match instruments:
  - Kt. St. 2 > “Violins”
  - Kt. St. 3 > “Violas”
  - Kt. St. 4 > “Trumpets”
  - Kt. St. 5 > “Horns”
  - Kt. St. 6 > “Flutes”
  - (Continue for all outputs)

### Result

- MIDI tracks in “Orchestra Folder” trigger articulations in one Kontakt instance.
- Each instrument outputs to its own Cubase mixer channel via St. 2 onward.
- Adjust Quantity in Step 3 based on your total instruments/articulations.

### Mixer volumes with Midi Tracks

- Go to Mixer (F3)
- Select the Routing section above the slider
- Select the "All Midi Input" dropdown and select a Channel that matches the Midi Track's assignment in Kontakt
- **You need to have Audio Outputs routed in the Kontakt instrument for this to work!**
  - MIDI channels only control which notes Kontakt listens to—they don’t affect volume sliders in Cubase’s mixer. If you want separate volume control for each instrument, you need to route each Kontakt instrument to its own audio output channel, not just a separate MIDI channel.
  - In Kontakt, open the Outputs panel, create separate outputs for each instrument, and route each instrument there. Then, Cubase will show individual audio faders for each instrument, letting you control volume directly.

### Troubleshooting no sound but right channel is selected:

- Make sure the instrument track and the Midi Tracks are all Record Enabled (click the circle record button and make sure it is highlighted red)

## Optimizing RAM

- Purge samples (i.e. in Kontakt)
- Load instruments into a Rack instrument. See [vid](https://www.udemy.com/course/cubase-complete-course/learn/lecture/34818318#notes)
- Can create individual instrument tracks, but you need to disable them to save ram.

## Adding Pitch Bend Wheel to Instrument

- open your desired instrument patch in Kontakt and click on the little wrench icon in the top left corner of the instrument.
- Once you’re there, move your cursor to the right until you find "Edit all Groups". Click on that. It’ll turn red.
- Now for the final step. Mosey on down to the "Source" menu and click the "Mod" button. You might see some stuff there already. Don’t pay it any mind.
  - Move your cursor down to "add modulator ...". Under "External Sources", click on "pitch bend".
- You should now have pitch bend working with the wheel for that instrument.

## Keyboard Shortcuts

- Move to beginning of track: Shift-B
