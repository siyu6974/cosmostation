---
title: evora_autofocus_1
date: 2024-02-26 22:10:59
tags:
skip_render: true
---
# Evora Autofocus Phase I: Focus assist

[GitHub - siyu6974/evora_autofocus](https://github.com/siyu6974/evora_autofocus#usage-version-01-awful-architecture-i-know-d)

![(Semi) Final result. 2023-10-21T09-00-13_B_-79.25_60.0s_0072.fits. FWHM: 3.0 HFD: 2.40](Untitled.png)

# Method

- FWHM
    - Full width half maximum
    - Astropy has it
    
    ![Star Profile](Untitled1.png)
    
    ![[https://www.lost-infinity.com/night-sky-image-processing-part-5-measuring-fwhm-of-a-star-using-curve-fitting-a-simple-c-implementation/](https://www.lost-infinity.com/night-sky-image-processing-part-5-measuring-fwhm-of-a-star-using-curve-fitting-a-simple-c-implementation/)](Untitled2.png)
    
- HFD / HFR
    - Half flux diameter or radius
    - general concept
        - [https://www.lost-infinity.com/night-sky-image-processing-part-6-measuring-the-half-flux-diameter-hfd-of-a-star-a-simple-c-implementation/](https://www.lost-infinity.com/night-sky-image-processing-part-6-measuring-the-half-flux-diameter-hfd-of-a-star-a-simple-c-implementation/)
        - [http://www.ccdware.com/Files/ITS Paper.pdf](http://www.ccdware.com/Files/ITS Paper.pdf)
        - more tolerant to out of focus star, especially for cassegrain
    - Implementation to achieve better sub pixel accuracy, not yet implemented
        - sorting based [https://github.com/OpenPHDGuiding/phd2/blob/5576bc0832c78b009e30687ac6b30404cb9e8fcd/star.cpp#L83](https://github.com/OpenPHDGuiding/phd2/blob/5576bc0832c78b009e30687ac6b30404cb9e8fcd/star.cpp#L83)
        - interpolation based: NINA [https://bitbucket.org/Isbeorn/nina/src/master/NINA.Core.WPF/ViewModel/AutoFocus/](https://bitbucket.org/Isbeorn/nina/src/master/NINA.Core.WPF/ViewModel/AutoFocus/)

# Evora image test

This was to test star detection and the correlation between FWHM and HFD on evora images. Test image `2023-05-20T09-32-28_r_-81.19_250.0s_r.fits`

[single_image_test.ipynb](single_image_test.ipynb)

![M57 test](Untitled3.png)

![M57 test graph](Untitled4.png)

The DAOStarFinder seems fine. FWHM is fairly consistent across the image. HFD has some weird negative values but the overall trend correlates with FWHM so it’s good. 

# Home test

Prior to the field test, a test was conducted at home to validate the method and general implementation of the algorithm.  

The optic train consists of a Askar 65phq telescope (D=65mm, F/6.4) and a Qhy533M cooled CMOS camera. ~~Data was collected while performing auto focus routine in NINA with hocus focus plugin.~~  Focus was adjusted manually by commanding the ZWO EAF to advance inward and outward. The sweep was not mono-directional but backlash should be compensated automatically by NINA. After each movement, a 2 second exposure was taken with L filter. 

[focus_test.ipynb](focus_test.ipynb)

![nice round tight stars](Untitled5.png)

![out of focus example](Untitled6.png)

![FWHM predicted 13678.46
HFD predicted 13670.96](Untitled7.png)

Results given by hocus focus on 2 others runs 2 hours later: 13636 for R, 13701 for L. 

Without any modification to HFD calculation, the negative numbers disappeared. Great?

Near the focus point, HFDs were almost flat, which is probably caused by the lack of precision of the current implementation. Need to go sub pixel.  

# MRO field test

## Initial test on 5s V-band exposures

![Screenshot 2023-10-25 at 16.54.38.png](Screenshot_2023-10-25_at_16.54.38.png)

Initial result was awful. 2 fits didn’t agree with each other, HFD values were nonsense. FWHM were also off, even if we excluded the outliner. 

Checking the intermediate steps, the DAOStarFinder was picking noise as stars. Tuning the parameters (#brightest, fwhm, std) didn’t help at all, and the selection was not consistent across the sweep. 

## Hot fix with sep - thanks José!

[mro_single_image_test.ipynb](mro_single_image_test.ipynb)

[mro_first_field_test.ipynb](mro_first_field_test.ipynb)

![comma or seeing?](Untitled8.png)

![Untitled](Untitled9.png)

![sep thinks this is 40pix big](Untitled10.png)

Sep worked wonder, with min-pix it’s even like black magic. This finally allowed the following calculation to work.

Stars are in bad shape, not sure if it’s seeing that’s tearing them apart. Longer exposure should help but takes more patience…

![Untitled](Untitled11.png)

HFD values are completely unusable, guess the noise was fooling my naive implementation. But FWHM seems like an OK fit.

## Real exposure

![Eyeballed. 2023-10-21T08-57-43_B_-79.25_60.0s_0071.fits. FWHM: 4.2](Untitled12.png)


![Calculated. 2023-10-21T09-00-13_B_-79.25_60.0s_0072.fits. FWHM: 3.0](Untitled.png)

Much better!

Note: the focuser position was calculated on V band, the above exposure was on B so the final image could be even better.

# TODO

- [ ]  sweep all filters, make an offset table
- [ ]  make better UI & integrate into evora
- [ ]  sub pixel HFD

# After first field test

October 31, 2023 

The hot fix using SEP and parameters that worked at MRO doesn’t work for my setup

- Too many stars
- FWHM fit can produce extreme outliers

Solutions

- limit source extraction output
- use median FWHM

HFD

- Issue with previous HFD calculation: pixel distance set to the top left corner of the aperture, should be the center
- Phd2 implementation: [https://github.com/OpenPHDGuiding/phd2/blob/5576bc0832c78b009e30687ac6b30404cb9e8fcd/star.cpp#L11](https://github.com/OpenPHDGuiding/phd2/blob/5576bc0832c78b009e30687ac6b30404cb9e8fcd/star.cpp#L113)[3](https://github.com/OpenPHDGuiding/phd2/blob/5576bc0832c78b009e30687ac6b30404cb9e8fcd/star.cpp#L83)
- **`sep.flux_radius` is fast**

![previous](Untitled13.png)

previous

![sep extraction, median](Untitled14.png)

sep extraction, median
