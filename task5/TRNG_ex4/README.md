Repository for Exercise 1.4 of Embedded Cryptography Book Section 9

In this exercise, you can play with a Monobit test such as the one required in the AIS31 and FIPS 140-1 test suites. 

By scanning or clicking on the QR-code you can launch the application and observe how the threshold and the block size are affecting the error Type 1 and 2 that are introduced in Section 1.6 of this chapter.

<p>This test triggers alarm if the number of bits equal to 1 is bigger than <sup>1</sup>&#8260<sub>2</sub> &#x22C5 Number_of_inputs_bits + relative_threshold or smaller than <sup>1</sup>&#8260<sub>2</sub> &#x22C5 Number_of_inputs_bits-relative_threshold.</p>


<p>Your goal is to find the the lowest relative_threshold allowing to have &#x3B1 bigger than 10<sup>-6</sup> and you should note the highest H<sub>1</sub> for which &#x3B2 is smaller than 10<sup>-6</sup>.</p>
  
<p>This H<sub>1</sub> will be the lowest entropy rate at TRNG output, which will not trigger alarm.</p>
<p>You should repeat the procedure for block_sizes=4096, 8192, 16384 and 32768.</p>



<p><a href="https://mybinder.org/v2/gh/patrickhaddadteaching/TRNG_ex4/main?urlpath=voila%2Frender%2FTRNG_ex4_nb.ipynb" target="_blank" rel="noopener noreferrer">  <img src="ex4.png" width="50%" height="50%"></a></p>
