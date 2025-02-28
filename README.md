# Visual_Inspection_Helper
Go through a directory of images and add flags/notes/redshifts to a periodically savable csv file

# From base anaconda environment:
### Should Already Have TKinter
### Requires: 

Python - conda install python

PIL - conda install pillow

pandas - conda install pandas

pdf2image - conda install -c conda-forge pdf2image (only if using \_pdf.py) 



# To Run:
`python vis_inspect_pdf.py`

This will create a window from which you can enter a file path or you can click `Browse Folders` to select a directory that *only* has pdf files in it. Once selected, click `Set File Path`.  

Next, a window titled [OIII] Visual Inspection will pop up.  (Because I'm using it for [OIII] visual inspection, specifically.) In this window, you can add Flags, Notes, and a nominal Redshift in each of the entry boxes on the left.  On the right is the pdf image.  When satisfied, click `Next` to go to the next file.  

Each time you click `Next`, the entries will be saved into a working  dictionaryobject.  
>**Alert: This is not saved to storage until you click `Save` or `Exit`**.  

You can go back to a previous source by clicking `Back`.
> **Note: If you have entered information and then go back to a previous source, when you come forward again, you will need to _re-enter_ the information again.**

Once you are at the end of the file list, the `Next` tab will turn to `Last Image` and will become obsolete.  You need to use the `Save` button to save the working dictionary into a csv file.  

**!!Known Bug!!  You must save the dictionary twice.**  The first time, it sometimes saves as an empty text file.  Click `Save` again and overwrite the first file.  Then it will save correctly. 

Once saved, you can click `Exit` which will force you to save it again and will close the window.  You will be left with the first window again and you can choose another directory to inspect.  When finished, simply use the `X` to close the window and end the program. 
