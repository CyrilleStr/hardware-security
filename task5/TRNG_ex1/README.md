Repository for Exercise 1.1 of Embedded Cryptography Book Section 9

In this exercise, you can play with an EO-TRNG.
By scanning or clicking on the QR-code you can launch the application and observe how the duty cycle,the jitter variance and the accumulation time affect randomness of the generated numbers. 
The randomness is analyzed by observing the distribution and the auto-correlation of generated 4-bit bit-vectors.

Note: In the case of an ideal RNG, the distribution and the auto-correlation are in 99.9% cases between the red lines.

Your goal is to find the the smallest D, for which the EO-TRNG would not be distinguishable from an ideal RNG.
<p>You should repeat the procedure for all possible <sup>&#x3C3<sub>tot</sub></sup> &#8260 <sub>T<sub>1</sub></sub> and 	&#x3B1<sub>1</sub> values.</p>





<p><a href="https://mybinder.org/v2/gh/patrickhaddadteaching/TRNG_ex1/main?urlpath=voila%2Frender%2FTRNG_ex1_nb.ipynb" target="_blank" rel="noopener noreferrer">  <img src="ex1.png" width="50%" height="50%"></a></p>
