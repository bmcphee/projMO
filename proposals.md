
+ Predictive text matching:
==========================

    + Given a dictionary of text as well as a query word, compute the edit distance
      between the each sequence and return words whose edit distance is greater than or equal
      to the threshold fuzziness.
      Text will be typed by the Arduino then sent over to the back-end for processing from which
     results will be returned and displayed onto the Arduino.

    This task incorporates the problem of computing edit distances, efficient computation and
    even providing user experience for a real time request systems, on memory constrains.


+ Mail routing:
================

    + Given a map and a post man to deliver mail with different priorities, compute an efficient
     route for the mail man to deliver the mail. This will involve finding optimal paths/shortest routes.
     However, the mail itself factors in because customers paid different amounts and even priorities 
     matter.


+ Baby monitor:
====================
    
    + Given a few peripherals like a microphone and camera, if a baby cries say persistenly or is scared
    the baby monitor should send an email to the parents or even send them a text message.
    To accomplish this, we'll be using a Raspberry Pi and PiCamera the Python module, as well as a microphone.

+ Duplicate name agnostic FS:
===============================

    + Ordinary user space file systems map filename and directory for uniqueness of a file. However,
    the ordinary user without having to have a CS degree would like to store clashing paths in the 
    same folder. I've encountered this problem in the real world when working on projects that involve
    syncing from the cloud, as well as uploading from some devices e.g iOS devices that abstract away filepaths. The basic logic will involve mapping a file to its randomly generated non-clashing UUID and the name and other attributes are non-unique.

+ Web indexer + Crawler:
========================
    + A custom web crawler. Will consist of a url extractor, link follower, indexer. 
