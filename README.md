# ScreenScroll
A text feature for blender to add in a "Typing" effect with loads of little tools

![Image](https://github.com/user-attachments/assets/fce2fe0b-9eff-4d98-bea3-53e77a514760)

**USE:**
Create a Text Object

Go to the "Data" tab
<img width="543" height="898" alt="Image" src="https://github.com/user-attachments/assets/b4b22d95-6aa8-4f7f-9092-15db77d0a948" />

Drop down "ScreenScroll Effect"
<img width="414" height="377" alt="Image" src="https://github.com/user-attachments/assets/cb9d245c-2b49-4af9-a2c1-4b94b6ba4027" />

Make sure the top check mark is enabled to turn it on!
<img width="417" height="443" alt="Image" src="https://github.com/user-attachments/assets/7949880c-24ac-4072-aaf8-fb926d2ceda5" />

Go to your Scripting Tab
<img width="1284" height="218" alt="Image" src="https://github.com/user-attachments/assets/91c525e7-8b33-4299-bc3f-8691e55df20b" />

Click the new button and make a new script!
<img width="1071" height="305" alt="Image" src="https://github.com/user-attachments/assets/04d1a5a0-df45-414e-a8ac-047fccd1d1f2" />

Put any and all text you want in the new script you make!

In "Text Source" on the ScreenScroll Effect page look for the new script you just made
<img width="409" height="399" alt="Image" src="https://github.com/user-attachments/assets/0914dbb2-e830-46a5-9bf5-e07db5b656f0" />

Go nuts!


start frame: Select what frame your text starts its scroll

letters per second: Determines how fast the letters type

delete mode: makes it look like the text is being deleted instead of added

reverse mode: types it bottom > top motion instead of the normal top > bottom (it doesnt like to work with scroll mode but im working on it)

loop mode: if it runs outta stuff to type, itll just type it again
  (loop delay: how long it takes to type the next sentence)

sentence cycle: at the end of a sentence it will delete that sentence and then type out the next one

scroll mode: scrolls the text upwards and deletes it after selected line length 
  (max lines: how many lines it shows before it scrubs upwards)

blinking cursor: adds a cursor at the end of the typing lines
 (cursor style: adds a couple of vatiations to the blinking cursor, including adding your own custom cursor)
  (cursor blink speed: how fast the cursor flashes)


random delay: lets you add variation to the speed between each typed letter so it can feel more "human"
  (random delay amount: pick how big the delay can be)
