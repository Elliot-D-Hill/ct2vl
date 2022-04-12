# ct2vl: Ct values to viral load
A command line tool and python package to convert SARS-CoV-2 Ct values to viral load.

## Usage

### Command line tool

To calibrate ct2vl run

    python3 -m ct2vl calibrate Ct_L v_L example/path/to/data

For example

    python3 -m ct2vl calibrate 37.96 100.0 positive_traces_with_ct_values.csv

Once ct2vl has been calibrated, Ct values can we converted to viral loads with

    python3 -m ct2vl convert Ct

One or multiple Ct values can be passed. For example

    python3 -m ct2vl convert 23.1
or

    python3 -m ct2vl convert 23.1 31.8 28.4 34.0 30.2

Output can saved to a file by providing a filepath to the optional flag `--output`

  python3 -m ct2vl convert 23.1 --output Results/viral_loads.tsv

### Python package
```python
    from ct2vl.ct2vl import CT2VL
    from pandas import read_csv

    traces = pd.read_csv('Data/positive_traces_with_ct_values.csv')
    converter = CT2VL(traces, Ct_at_LoD=37.96, LoD=100.0)
    ct_values = [23.1, 31.8, 28.4, 34.0, 30.2]
    viral_load = converter.convert(ct_values)
```

## Input

The command line tool has two modes `calibrate` and `convert`.

* `mode`: `calibrate` uses positive PCR traces and their corresponding Ct values to calibrate ct2vl for a given machine
   1. `Ct_at_LoD`: Ct value at the limit of detection (LoD)
   2. `LoD`: Limit of detection (LoD): copies of SARS-CoV-2 viral genomes/mL (copies/mL; viral load at the LoD)
   3. `infile`: Filepath to a csv file containing Ct values and PCR reaction traces
* `mode`: `convert` calculates the viral loads for given Ct values
    1. `Ct`: A list of Ct values that will be converted to viral loads
    2. `--outfile`: An optional filepath to save the results to

For `calibrate` mode, `infile` is a csv file where each row corresponds to a run and the first column contains the Ct values for each run and the remaining columns contain the values at each cycle.

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ct_value</th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
      <th>8</th>
      <th>...</th>
      <th>29</th>
      <th>30</th>
      <th>31</th>
      <th>32</th>
      <th>33</th>
      <th>34</th>
      <th>35</th>
      <th>36</th>
      <th>37</th>
      <th>38</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>27.68</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.036339</td>
      <td>0.105185</td>
      <td>0.140072</td>
      <td>0.213080</td>
      <td>...</td>
      <td>75.820797</td>
      <td>103.521744</td>
      <td>128.057320</td>
      <td>146.543328</td>
      <td>158.994255</td>
      <td>166.878167</td>
      <td>171.755301</td>
      <td>174.695708</td>
      <td>176.480445</td>
      <td>178.004733</td>
    </tr>
    <tr>
      <th>1</th>
      <td>33.71</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.032859</td>
      <td>0.106156</td>
      <td>0.115075</td>
      <td>...</td>
      <td>1.498253</td>
      <td>3.242639</td>
      <td>6.929736</td>
      <td>14.413807</td>
      <td>26.735120</td>
      <td>42.908856</td>
      <td>60.642276</td>
      <td>77.436979</td>
      <td>90.894471</td>
      <td>98.702497</td>
    </tr>
    <tr>
      <th>2</th>
      <td>13.24</td>
      <td>0.008563</td>
      <td>0.077690</td>
      <td>0.112795</td>
      <td>0.112795</td>
      <td>0.112795</td>
      <td>0.112795</td>
      <td>0.112795</td>
      <td>0.112795</td>
      <td>0.250068</td>
      <td>...</td>
      <td>239.545742</td>
      <td>240.219129</td>
      <td>240.706006</td>
      <td>241.006463</td>
      <td>241.206473</td>
      <td>241.304155</td>
      <td>241.389261</td>
      <td>241.421420</td>
      <td>241.421420</td>
      <td>241.421420</td>
    </tr>
    <tr>
      <th>3</th>
      <td>22.50</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.043038</td>
      <td>0.061215</td>
      <td>0.061215</td>
      <td>0.061215</td>
      <td>0.061215</td>
      <td>0.061215</td>
      <td>0.061215</td>
      <td>...</td>
      <td>177.787281</td>
      <td>185.406029</td>
      <td>190.989406</td>
      <td>195.223471</td>
      <td>198.308876</td>
      <td>200.551725</td>
      <td>202.243363</td>
      <td>203.463125</td>
      <td>204.342186</td>
      <td>205.015795</td>
    </tr>
    <tr>
      <th>4</th>
      <td>23.08</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.014523</td>
      <td>0.038724</td>
      <td>0.083699</td>
      <td>0.116689</td>
      <td>0.131569</td>
      <td>0.131569</td>
      <td>...</td>
      <td>173.993467</td>
      <td>183.424795</td>
      <td>190.361277</td>
      <td>195.482481</td>
      <td>199.194926</td>
      <td>201.862966</td>
      <td>203.861077</td>
      <td>205.329761</td>
      <td>206.289263</td>
      <td>206.824331</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>16</th>
      <td>21.53</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.050974</td>
      <td>0.085428</td>
      <td>0.085428</td>
      <td>0.085428</td>
      <td>0.085428</td>
      <td>0.085428</td>
      <td>0.085428</td>
      <td>...</td>
      <td>194.717208</td>
      <td>201.251802</td>
      <td>206.238474</td>
      <td>209.977472</td>
      <td>212.850522</td>
      <td>214.995915</td>
      <td>216.711037</td>
      <td>217.980163</td>
      <td>218.880729</td>
      <td>219.491032</td>
    </tr>
    <tr>
      <th>17</th>
      <td>23.39</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.080598</td>
      <td>0.126204</td>
      <td>0.224708</td>
      <td>0.254782</td>
      <td>...</td>
      <td>187.883601</td>
      <td>199.664452</td>
      <td>208.208690</td>
      <td>214.361070</td>
      <td>218.809716</td>
      <td>222.239450</td>
      <td>224.701419</td>
      <td>226.574815</td>
      <td>227.972374</td>
      <td>229.085984</td>
    </tr>
    <tr>
      <th>18</th>
      <td>28.46</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.092015</td>
      <td>0.215467</td>
      <td>0.297682</td>
      <td>...</td>
      <td>51.416916</td>
      <td>80.692981</td>
      <td>112.770737</td>
      <td>142.339464</td>
      <td>165.674804</td>
      <td>182.084870</td>
      <td>193.083210</td>
      <td>200.171681</td>
      <td>204.779740</td>
      <td>208.237394</td>
    </tr>
    <tr>
      <th>19</th>
      <td>27.86</td>
      <td>0.443534</td>
      <td>0.443534</td>
      <td>0.443534</td>
      <td>0.443534</td>
      <td>0.443534</td>
      <td>0.443534</td>
      <td>0.443534</td>
      <td>0.443534</td>
      <td>0.443534</td>
      <td>...</td>
      <td>70.164310</td>
      <td>97.490787</td>
      <td>122.766640</td>
      <td>142.936795</td>
      <td>157.475829</td>
      <td>167.632976</td>
      <td>174.804737</td>
      <td>179.870366</td>
      <td>183.435423</td>
      <td>186.212804</td>
    </tr>
    <tr>
      <th>20</th>
      <td>15.61</td>
      <td>0.000000</td>
      <td>0.060721</td>
      <td>0.060721</td>
      <td>0.064403</td>
      <td>0.064403</td>
      <td>0.064403</td>
      <td>0.064403</td>
      <td>0.064403</td>
      <td>0.064403</td>
      <td>...</td>
      <td>225.043424</td>
      <td>226.333617</td>
      <td>227.403273</td>
      <td>228.214905</td>
      <td>228.866112</td>
      <td>229.370140</td>
      <td>229.680560</td>
      <td>229.890248</td>
      <td>229.967121</td>
      <td>229.967121</td>
    </tr>
  </tbody>
</table>
</div>


## Output

The command line tool output is tab separated and is pipable, e.g.,

    python3 -m ct2vl convert 23.1 31.8 28.4 34.0 30.2 > results.tsv

The function `convert_ct2vl` in the python package returns the results in a pandas dataframe.

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ct_value</th>
      <th>viral_load</th>
      <th>lower_95_ci</th>
      <th>upper_95_ci</th>
      <th>log10_viral_load</th>
      <th>log10_lower_95_ci</th>
      <th>log10_upper_95_ci</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>23.1</td>
      <td>777543.433255</td>
      <td>580181.755636</td>
      <td>906810.381296</td>
      <td>5.890725</td>
      <td>5.763564</td>
      <td>5.957516</td>
    </tr>
    <tr>
      <th>1</th>
      <td>31.8</td>
      <td>4100.957983</td>
      <td>3637.233018</td>
      <td>4365.686911</td>
      <td>3.612885</td>
      <td>3.560771</td>
      <td>3.640053</td>
    </tr>
    <tr>
      <th>2</th>
      <td>28.4</td>
      <td>31848.519825</td>
      <td>26414.830590</td>
      <td>35121.013807</td>
      <td>4.503089</td>
      <td>4.421848</td>
      <td>4.545567</td>
    </tr>
    <tr>
      <th>3</th>
      <td>34.0</td>
      <td>1088.582988</td>
      <td>1007.991378</td>
      <td>1133.030544</td>
      <td>3.036862</td>
      <td>3.003457</td>
      <td>3.054242</td>
    </tr>
    <tr>
      <th>4</th>
      <td>30.2</td>
      <td>10759.870164</td>
      <td>9247.366373</td>
      <td>11645.316301</td>
      <td>4.031807</td>
      <td>3.966018</td>
      <td>4.066151</td>
    </tr>
  </tbody>
</table>
</div>

