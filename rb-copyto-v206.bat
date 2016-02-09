mkdir c:\temp\rblogs

xcopy C:\n\Dropbox\csd\VCS-git\pdb218 \\PMDS-DATA\p2\xampp\htdocs\python\pdb218   /s/e/d/h/i/f/c/k/y 
xcopy C:\n\Dropbox\csd\VCS-git\pdb218 \\pmdsdata3\html\python\pdb218              /s/e/d/h/i/f/c/k/y 

robocopy C:\n\Dropbox\csd\VCS-git\pdb218 \\PMDS-DATA\p2\xampp\htdocs\python\pdb218  /l  /COPY:DT /xd  templates_c /fft /dst /xo /ndl /np /r:0 /w:9 /tee /log:"c:\temp\rblogs\pdb218-%dhms%-%random%-%random%"

:robocopy C:\n\Dropbox\csd\VCS-git\pdb218 \\PMDS-DATA\p2\xampp\htdocs\python\pdb218   /e  /COPY:DT /xd .git templates_c testnobackup /fft /dst /xo /ndl /np /r:0 /w:9 /tee /log:"c:\temp\rblogs\pdb218-%dhms%-%random%-%random%"

robocopy C:\n\Dropbox\csd\VCS-git\pdb218 \\v206b2\html\python\pdb218   /e  /COPY:DT /xd .git templates_c testnobackup /fft /dst /xo /ndl /np /r:0 /w:9 /tee /log:"c:\temp\rblogs\pdb218-%dhms%-%random%-%random%"

pause
