# ADS Name Tags

Small script that makes door name tags using our logo. If you supply a github handle,
it will download the users gravatar from github, if it exists, and place it within
the circle of the ADS logo.

A PDF document is created for all users requested, so that it can be easily printed,
and the tags cut out.

### Usage
```
python nametag.py -p Bumble Rocket, test
```
Results in an image like this, with an accompanying PDF:

[BumbleRocket](Bumble_Rocket-name-tag.jpg)

For multiple users, simply repeat the flag:

```bash
python nametag.py -p Bumble Rocket, test -p Steve Jobs, sjobs -p Bill Gates
```

In this example Bill does not use git, but svn, and so no github handle has been passed - its optional.
In this scenario, no image is placed within the circle of the ADS logo.


### Requirements
 * TeXLive with PDFLaTeX available
