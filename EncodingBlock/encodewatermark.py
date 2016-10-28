from scipy.io.wavfile import read,write
import exceptions
import sys
import numpy
from sklearn.svm import SVC
from scipy.fftpack import fft,ifft
from scipy.fftpack.realtransforms import dct
from math import pow,exp
# from constants import TH
N_SUBBAND = 8

Win                  = 512
HalfWin              = 256

eps                  = 0.00000001
bark_array           = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
critical_freq        = [50,150,250,350,450,570,700,840,1000,1170,1370,1600,1850,2150,2500,2900,3400,4000,4800,5800,7000,8500,10500,13500]
frequency_array      = [0.0, 86.1328125, 172.265625, 258.3984375, 344.53125, 430.6640625, 516.796875, 602.9296875, 689.0625, 775.1953125, 861.328125, 947.4609375, 1033.59375, 1119.7265625, 1205.859375, 1291.9921875, 1378.125, 1464.2578125, 1550.390625, 1636.5234375, 1722.65625, 1808.7890625, 1894.921875, 1981.0546875, 2067.1875, 2153.3203125, 2239.453125, 2325.5859375, 2411.71875, 2497.8515625, 2583.984375, 2670.1171875, 2756.25, 2842.3828125, 2928.515625, 3014.6484375, 3100.78125, 3186.9140625, 3273.046875, 3359.1796875, 3445.3125, 3531.4453125, 3617.578125, 3703.7109375, 3789.84375, 3875.9765625, 3962.109375, 4048.2421875, 4134.375, 4220.5078125, 4306.640625, 4392.7734375, 4478.90625, 4565.0390625, 4651.171875, 4737.3046875, 4823.4375, 4909.5703125, 4995.703125, 5081.8359375, 5167.96875, 5254.1015625, 5340.234375, 5426.3671875, 5512.5, 5598.6328125, 5684.765625, 5770.8984375, 5857.03125, 5943.1640625, 6029.296875, 6115.4296875, 6201.5625, 6287.6953125, 6373.828125, 6459.9609375, 6546.09375, 6632.2265625, 6718.359375, 6804.4921875, 6890.625, 6976.7578125, 7062.890625, 7149.0234375, 7235.15625, 7321.2890625, 7407.421875, 7493.5546875, 7579.6875, 7665.8203125, 7751.953125, 7838.0859375, 7924.21875, 8010.3515625, 8096.484375, 8182.6171875, 8268.75, 8354.8828125, 8441.015625, 8527.1484375, 8613.28125, 8699.4140625, 8785.546875, 8871.6796875, 8957.8125, 9043.9453125, 9130.078125, 9216.2109375, 9302.34375, 9388.4765625, 9474.609375, 9560.7421875, 9646.875, 9733.0078125, 9819.140625, 9905.2734375, 9991.40625, 10077.5390625, 10163.671875, 10249.8046875, 10335.9375, 10422.0703125, 10508.203125, 10594.3359375, 10680.46875, 10766.6015625, 10852.734375, 10938.8671875, 11025.0, 11111.1328125, 11197.265625, 11283.3984375, 11369.53125, 11455.6640625, 11541.796875, 11627.9296875, 11714.0625, 11800.1953125, 11886.328125, 11972.4609375, 12058.59375, 12144.7265625, 12230.859375, 12316.9921875, 12403.125, 12489.2578125, 12575.390625, 12661.5234375, 12747.65625, 12833.7890625, 12919.921875, 13006.0546875, 13092.1875, 13178.3203125, 13264.453125, 13350.5859375, 13436.71875, 13522.8515625, 13608.984375, 13695.1171875, 13781.25, 13867.3828125, 13953.515625, 14039.6484375, 14125.78125, 14211.9140625, 14298.046875, 14384.1796875, 14470.3125, 14556.4453125, 14642.578125, 14728.7109375, 14814.84375, 14900.9765625, 14987.109375, 15073.2421875, 15159.375, 15245.5078125, 15331.640625, 15417.7734375, 15503.90625, 15590.0390625, 15676.171875, 15762.3046875, 15848.4375, 15934.5703125, 16020.703125, 16106.8359375, 16192.96875, 16279.1015625, 16365.234375, 16451.3671875, 16537.5, 16623.6328125, 16709.765625, 16795.8984375, 16882.03125, 16968.1640625, 17054.296875, 17140.4296875, 17226.5625, 17312.6953125, 17398.828125, 17484.9609375, 17571.09375, 17657.2265625, 17743.359375, 17829.4921875, 17915.625, 18001.7578125, 18087.890625, 18174.0234375, 18260.15625, 18346.2890625, 18432.421875, 18518.5546875, 18604.6875, 18690.8203125, 18776.953125, 18863.0859375, 18949.21875, 19035.3515625, 19121.484375, 19207.6171875, 19293.75, 19379.8828125, 19466.015625, 19552.1484375, 19638.28125, 19724.4140625, 19810.546875, 19896.6796875, 19982.8125, 20068.9453125, 20155.078125, 20241.2109375, 20327.34375, 20413.4765625, 20499.609375, 20585.7421875, 20671.875, 20758.0078125, 20844.140625, 20930.2734375, 21016.40625, 21102.5390625, 21188.671875, 21274.8046875, 21360.9375, 21447.0703125, 21533.203125, 21619.3359375, 21705.46875, 21791.6015625, 21877.734375, 21963.8671875, 22050.0]
bark_array_float     = [0.0, 0.85024138263826743, 1.6942053376831454, 2.5250507034992236, 3.3366115985833695, 4.1236353554724543, 4.8819244376466751, 5.608381492206866, 6.3009708527794768, 6.9586182220227455, 7.5810726534355322, 8.1687527011726822, 8.722593747945556, 9.2439079106215232, 9.734262823448546, 10.195381630314646, 10.629063811518868, 11.037124874320256, 11.421352182763128, 11.783474017052161, 12.125139107984586, 12.447904220682455, 12.753227753802294, 13.042467709685686, 13.316882742999283, 13.577635295920418, 13.825796074404989, 14.062349316406126, 14.288198455775447, 14.504171902397042, 14.711028746947491, 14.909464263758057, 15.100115132777239, 15.283564335802062, 15.46034570629039, 15.630948128765709, 15.795819395055926, 15.955369731863527, 16.10997501856599, 16.259979716524793, 16.405699532151548, 16.547423835988837, 16.685417859435859, 16.819924689717944, 16.951167082429798, 17.079349109590627, 17.204657659714915, 17.327263804978823, 17.447324049184004, 17.564981468909391, 17.680366759009619, 17.79359919247182, 17.904787503582391, 18.014030702380612, 18.121418827483769, 18.227033643554506, 18.330949288942222, 18.433232878359775, 18.53394506485289, 18.633140564775392, 18.730868648996868, 18.827173603135677, 18.922095159225808, 19.015668900888357, 19.107926643783284, 19.198896792862168, 19.288604677724667, 19.377072867197523, 19.464321464102326, 19.5503683810539, 19.635229598032712, 19.718919402398591, 19.801450611957243, 19.882834781652491, 19.963082394433126, 20.042203036831392, 20.12020555978809, 20.197098225264277, 20.272888839190419, 20.347584871317451, 20.421193562550346, 20.493722020360341, 20.565177302887214, 20.63556649235586, 20.704896758441453, 20.773175412224351, 20.840409951378476, 20.906608097236042, 20.97177782436577, 21.035927383292648, 21.09906531697386, 21.161200471628522, 21.222342002498927, 21.282499375097771, 21.341682362470536, 21.399901038974654, 21.457165771048214, 21.513487205410868, 21.568876255108933, 21.623344083785632, 21.676902088526578, 21.729561881600059, 21.781335271381931, 21.832234242726038, 21.882270937013267, 21.931457632086047, 21.979806722249897, 22.027330698500254, 22.074042129110744, 22.119953640698775, 22.16507789986553, 22.20942759549024, 22.253015421743065, 22.29585406186677, 22.337956172764585, 22.379334370420594, 22.420001216168703, 22.45996920381765, 22.49925074763183, 22.537858171160973, 22.575803696906277, 22.613099436805623, 22.649757383516707, 22.685789402473617, 22.721207224689696, 22.756022440277718, 22.790246492656763, 22.823890673414102, 22.856966117789909, 22.889483800752181, 22.921454533629223, 22.95288896126744, 22.983797559682451, 23.014190634172319, 23.044078317862446, 23.073470570652468, 23.102377178536678, 23.130807753270389, 23.158771732355881, 23.186278379322722, 23.213336784278315, 23.239955864705934, 23.266144366488422, 23.291910865137183, 23.317263767206946, 23.342211311878231, 23.366761572690297, 23.39092245940855, 23.414701720011326, 23.438106942782145, 23.461145558494209, 23.483824842675048, 23.506151917940013, 23.528133756384115, 23.549777182022499, 23.571088873270675, 23.592075365456157, 23.612743053354031, 23.633098193739329, 23.653146907950052, 23.672895184454813, 23.692348881419843, 23.711513729270632, 23.730395333243653, 23.748999175924329, 23.767330619767627, 23.785394909598075, 23.803197175086328, 23.820742433199733, 23.838035590624639, 23.855081446158408, 23.871884693069461, 23.888449921423749, 23.904781620376411, 23.920884180427443, 23.936761895640505, 23.952418965824087, 23.967859498674322, 23.983087511879095, 23.998106935183014, 24.012921612412992, 24.027535303464333, 24.041951686247252, 24.056174358593903, 24.070206840125959, 24.084052574083014, 24.097714929112026, 24.111197201018022, 24.124502614476594, 24.137634324708394, 24.150595419116193, 24.163388918884927, 24.176017780545227, 24.18848489750097, 24.200793101521406, 24.212945164198405, 24.224943798369448, 24.236791659506906, 24.248491347074257, 24.260045405849855, 24.271456327218822, 24.282726550433772, 24.293858463844906, 24.304854406100173, 24.315716667316103, 24.326447490219937, 24.337049071263653, 24.347523561710556, 24.357873068695028, 24.368099656256021, 24.378205346344899, 24.388192119808288, 24.398061917346418, 24.407816640447617, 24.417458152299496, 24.426988278677385, 24.436408808810555, 24.445721496226835, 24.454928059576055, 24.464030183432925, 24.473029519079816, 24.481927685269984, 24.490726268971628, 24.499426826093455, 24.508030882191996, 24.516539933161308, 24.524955445905434, 24.533278858994091, 24.541511583301954, 24.5496550026321, 24.557710474323823, 24.565679329845416, 24.573562875372183, 24.581362392350108, 24.589079138045559, 24.596714346081374, 24.604269226959708, 24.611744968571962, 24.619142736696134, 24.626463675481919, 24.633708907923946, 24.640879536323304, 24.647976642737863, 24.655001289421499, 24.661954519252671, 24.668837356152487, 24.675650805492655, 24.682395854493514, 24.689073472612407, 24.695684611922665, 24.702230207483492, 24.708711177700867, 24.715128424679836, 24.721482834568313, 24.727775277892697, 24.734006609885427, 24.740177670804755]
bark_array_int       = [0, 0, 1, 2, 3, 4, 4, 5, 6, 6, 7, 8, 8, 9, 9, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 14, 14, 15, 15, 15, 15, 15, 15, 16, 16, 16, 16, 16, 16, 16, 17, 17, 17, 17, 17, 17, 17, 17, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24]
threshold_quiet_vals = [0.00944567963877, 25.866905584234836, 14.845877790185327, 10.721316524988449, 8.502852236361942, 7.095039734397721, 6.110057817059093, 5.373618583691817, 4.7948098634808005, 4.320951394787291, 3.91894532646452, 3.5665698929651404, 3.2480334029873283, 2.9515476826576665, 2.6679398661655123, 2.3898359667120745, 2.111178657422631, 1.8269507493008739, 1.5330305890978444, 1.2261341466333364, 0.9038138277834085, 0.5644923360120119, 0.2075144738888888, -0.1667975824961104, -0.5570982493416764, -0.9609929584662045, -1.3750426339378354, -1.794805851953005, -2.2149239105396985, -2.629251204875492, -3.031030143399911, -3.4131065183602547, -3.7681779828149615, -4.089065333939351, -4.368993911448186, -4.601870816330641, -4.782543013475016, -4.90702180313606, -4.972660643003923, -4.978275792766078, -4.9242025639086755, -4.812283839916469, -4.645791682760887, -4.4292869319167885, -4.168425409498801, -3.8697223837834955, -3.540289091365426, -3.187556236719281, -2.818999431951775, -2.4418805581106096, -2.0630171565656132, -1.6885893961821015, -1.3239911550681212, -0.973728568644711, -0.641366285092746, -0.3295188608072511, -0.03988240010067545, 0.22670018646337686, 0.47014800682254054, 0.6910332246336232, 0.8904622751361903, 1.0699545692887857, 1.2313249688762915, 1.3765750516416309, 1.5077968159565356, 1.627091116063716, 1.7365018667426917, 1.8379659795469205, 1.9332781335420957, 2.0240688582804713, 2.1117940103796955, 2.1977335356205696, 2.2829973927971183, 2.3685366346118784, 2.4551578544491197, 2.5435394780773533, 2.634248673462246, 2.7277579436563464, 2.824460737940284, 2.924685652554163, 3.0287089879767137, 3.1367655831322034, 3.2490579600924065, 3.365763890161053, 3.487042539389939, 3.6130393747622103, 3.7438900175023617, 3.879723222648571, 4.020663148725649, 4.166831061730887, 4.318346596425363, 4.475328677026105, 4.637896180049153, 4.806168404944998, 4.980265403577698, 5.160308207528755, 5.346418982480119, 5.538721131274028, 5.737339361346369, 5.942399727770581, 6.154029659839783, 6.372357976700712, 6.597514895821029, 6.829632036847779, 7.068842422563367, 7.315280478061703, 7.569082028872243, 7.830384298496855, 8.099325905651252, 8.37604686139065, 8.660688566227691, 8.953393807305265, 9.254306755659014, 9.563572963587063, 9.881339362134174, 10.207754258691846, 10.542967334712019, 10.887129643530722, 11.240393608296788, 11.602913020000425, 11.97484303559668, 12.356340176218463, 12.747562325474533, 13.148668727827685, 13.559819987048746, 13.981178064742458, 14.412906278941138, 14.85516930276268, 15.308133163129432, 15.771965239544603, 16.246834262923464, 16.732910314476186, 17.23036482463989, 17.739370572057318, 18.260101682599643, 18.79273362843144, 19.3374432271154, 19.894408640755103, 20.46380937517382, 21.045826279127525, 21.640641543550657, 22.248438700832832, 22.869402624125136, 23.503719526674676, 24.15157696118574, 24.8131638192068, 25.488670330541623, 26.1782880626838, 26.882209920273443, 27.600630144574897, 28.333744312974904, 29.08174933849979, 29.844843469351275, 30.623226288459886, 31.417098713055022, 32.22666299425138, 33.05212271665051, 33.89368279795727, 34.751549488610394, 35.625930371426286, 36.51703436125615, 37.42507170465503, 38.35025397956305, 39.29279409499787, 40.25290629075797, 41.23080613713653, 42.22671053464509, 43.24083771374705, 44.273407234600235, 45.324639986808265, 46.394758189180614, 47.48398538950053, 48.59254646430101, 49.72066761864824, 50.86857638593213, 52.036501627664016, 53.224673533280814, 54.43332361995571, 55.66268473241508, 56.912991042761185, 58.18447805030071, 59.47738258137875, 60.79194278921803, 62.12839815376348, 63.48698948153127, 64.86795890546308, 66.27154988478446, 67.69800720486795, 69.14757697710012, 70.62050663875308, 72.11704495285944, 73.6374420080914, 75.1819492186434, 76.75081932411827, 78.344306389417, 79.96266580463129, 81.60615428493978, 83.2750298705072, 84.96955192638622, 86.68998114242277, 88.43657953316321, 90.20961043776504, 92.00933851990962, 93.83602976771763, 95.68995149366715, 97.57137233451324, 99.48056225121081, 101.41779252883896, 103.38333577652763, 105.37746592738665, 107.40045823843589, 109.45258929053816, 111.53413698833357, 113.64538056017574, 115.78660055806989, 117.95807885761211, 120.16009865793096, 122.39294448163001, 124.6569021747323, 126.95225890662633, 129.27930317001292, 131.63832478085408, 134.02961487832283, 136.45346592475462, 138.91017170559996, 141.40002732937782, 143.9233292276307, 146.48037515488093, 149.07146418858764, 151.69689672910536, 154.3569744996429, 157.05200054622406, 159.78227923764902, 162.54811626545626, 165.34981864388652, 168.18769470984626, 171.06205412287304, 173.97320786510144, 176.9214682412295, 179.90714887848694, 182.93056472660265, 185.99203205777425, 189.0918684666379, 192.23039287023852, 195.40792550800174, 198.62478794170505, 201.8813030554508, 205.17779505563934, 208.5145894709428, 211.89201315228007, 215.31039427279103, 218.77006232781278, 222.27134813485563, 225.81458383357983, 229.40010288577326, 233.02824007532854, 236.69933150822166]

#critical definitions, ie the index of the frequency array that has 
#the frequency closest to the corresponding critical band rate
#in bark
criticaldefn         = [1, 2, 3, 4, 5, 7, 8, 10, 12, 14, 16, 19, 21, 25, 29, 34, 39, 46, 56, 67, 81, 99, 122, 157]

# multiplier for the frames, B frames per unit, implies, 4 elements
C                    = [1,1,-1,-1]
U                    = 4    #no of frames per unit
B                    = 10   #no of units per block
mfccfilterbank_index = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 19, 20, 23, 25, 28, 30, 35, 37, 43, 46, 53, 57, 65, 70, 80]
Num_subbands         = 14
watermark_strength   = 5

frame_size           = 512
duration_block_point = B*U*frame_size/(2.0)

#read the wave file
def dataread(filename):
    try:
        data = read(filename)
        return data
    except IOError:
        print("IOError:Wrong file or file path")
        #TODO we will trace back and add codes for the exit code
        sys.exit()

def datawrite(filename,rate,data):
    try:
        write(filename, rate, data)
    except IOError:
        print("IOError:Wrong file or file path")
        #TODO we will trace back and add codes for the exit code
        sys.exit()

# Block to expand the bits obtained from the bit-expand block
def signexpanded(PNseq,N_unit,factor):
    tmp = []
    for i in range(Num_subbands):
        tmp.append(factor*PNseq[N_unit+(B*i)])

    sign = []
    for i in range(HalfWin):
        sign.append(1)

    for i in range(Num_subbands):
        for j in range(2*i,(2*i)+1):
            sign[j]=tmp[i];
    
    return sign

# Unused as the values of Fs and Win are fixed, the freq array is known
# they have been hardcoded for efficient computation
def frequency_axis(Fs,Win):
    frequency_array = []
    for i in range((Win/2)+1):
        frequency_array.append((i*Fs)/float(Win))
    return frequency_array

# Unused as the values the frequency array and the formula for threshold 
# in quiet are fixed, the threshold in quiet is known
# they have been hardcoded for efficient computation
def threshold_quiet(array_frequency,length):
    quiet_threshold = []
    quiet_threshold.append(0.00944567963877)
    for i in range(1,length):
        quiet_threshold.append((3.64*pow((array_frequency[i]/1000.0),-0.8))-(6.5*exp(-0.6*pow(((array_frequency[i]/1000.0)-3.3),2)))+(0.001*pow((array_frequency[i]/1000.0),4)))
    return quiet_threshold

# Unused as the values the frequency array and the formula for bark scale
# are fixed, the bark scale array is known
# they have been hardcoded for efficient computation
def bark(f):    
    "Convert a frequency from Hertz to Bark"
    return 13.0 * numpy.arctan(0.76 * f / 1000.0) + 3.5 * numpy.arctan((f / 7500.0) ** 2)

# Unused as the values the frequency array and the center frequency of 
# each bark are fixed, the frequncy value closest to centre frequncy in each bark is known
# they have been hardcoded for efficient computation
def closeto_critical(f):
    num = 0
    critical_close = []
    for i in range(len(f)):
        if(f[i]>critical_freq[num]):
            if(i-1>=0):
                if(numpy.mean([int(f[i]),int(f[i-1])])>critical_freq[num]):
                    x = (i-1)
                else:
                    x = (i)
            else:
                x = i
            critical_close.append(x)
            num+=1
            if(num==len(critical_freq)):
                break
    return critical_close


def hann(wave,length):
    for i in range(length):
        wave[i]=0.81649658092*(1-numpy.cos(2*numpy.pi*i/length))*wave[i]
    return wave

def SPL_normalise(wave_DB,length):
    maximum_value = max(wave_DB)
    for i in range(length):
        wave_DB[i]=96-maximum_value+wave_DB[i]
        # wave_DB[i] = wave_DB[i]
    return wave_DB,96-maximum_value


def tonal_markers_sound(wave_DB,length):
    # print wave_DB
    # if (length>252):
    #     length = 252
    val  = numpy.zeros(length)
    Pval = numpy.empty(length)

    # Figures if a point is a tonal maxima, allots a value of 1 to tonal and 0 to non tonal and 3 to irrelevant ones
    for i in range(2,62):
        if(val[i]!=3):
            c = 0
            if(wave_DB[i]-wave_DB[i+2]<7 or wave_DB[i]-wave_DB[i-2]<7):
                c = 1
            if c==0 :
                val[i] = 1
                val[i+1] = 3
            else :
                val[i] = 0

    for i in range(62,126):
        if(val[i] !=3):    
            c = 0
            if(wave_DB[i]-wave_DB[i+2]<7 or wave_DB[i]-wave_DB[i-2]<7 or wave_DB[i]-wave_DB[i+3]<7 or wave_DB[i]-wave_DB[i-3]<7):
                c = 1
            if c==0 :
                val[i] = 1
                val[i+1] = 3
                val[i+2] = 3
                val[i+3] = 3
            else :
                val[i] = 0

    for i in range(126,249):
        if(val[i] !=3):
            c = 0
            for j in range(2,7):
                if(wave_DB[i]-wave_DB[i+j]<7 or wave_DB[i]-wave_DB[i-j]<7):
                    c = 1
            if c==0 :
                val[i] = 1
                val[i+1] = 3
                val[i+2] = 3
                val[i+3] = 3
                val[i+4] = 3
                val[i+5] = 3
                val[i+6] = 3
            else :
                val[i] = 0

    for i in range(2,249):
        if(val[i]==1):
            Pval[i]   = 10*numpy.log10(pow(10,(wave_DB[i-1]/10.0))+pow(10,(wave_DB[i]/10.0))+pow(10,(wave_DB[i+1]/10.0)))

    # Selects only the non tonal masker that is closest to the central 
    # to every critical bandrate and adds up all the non tonals in that bin
    # into this one bin, and gives a marker of 2 to the central non tonal one
    sum1 = 0
    bark_prev = bark_array_int[0]
    for i in range(length):
        if(val[i]==0):
            if(bark_array_int[i]!=bark_prev):
                Pval[criticaldefn[bark_prev]]=10*numpy.log10(sum1)
                val[criticaldefn[bark_prev]]=2
                bark_prev = bark_array_int[i]
                sum1 = 0   
            Pval[i] = 0         
            sum1+=pow(10,(wave_DB[i]/10.0))

    # TODO -delete these
    # for i in range(len(criticaldefn)):
    #     print criticaldefn[i],Pval[criticaldefn[i]], float_barkarray[criticaldefn[i]],quiet_threshold[criticaldefn[i]]

    # removes the invalid tonal and non tonal markers
    # removes the ones below threshold of hearing and 
    # removes the smaller among the ones within 0.5 barks to each other
    count = 0
    for i in range(length):
        if(val[i]==1 or val[i]==2):
            if(Pval[i]<threshold_quiet_vals[i]):
                val[i] = 0
                Pval[i]= 0
            if(count>0):
                if(bark_array_float[valprev]-bark_array_float[i]<0.5):
                    if(Pval[valprev]>Pval[i]):
                        Pval[i] = 0
                        val[i]  = 0
                    else:
                        Pval[valprev]=0
                        val[valprev]=0
            count = count+1
            valprev = i
    return Pval,val
            
def compute_masking_indices(val,length):
    masking_indices  = numpy.empty(length)
    for i in range(length):
        if(val[i]==1):
           masking_indices[i]=((-6.025)-(0.275*bark_array_float[i]))
        elif(val[i]==2):
           masking_indices[i]=((-2.025)-(0.175*bark_array_float[i]))
    return masking_indices
    # 1 -2.17379224196
    # 3 -2.46688387311
    # 5 -2.74663618721
    # 8 -3.12766989924
    # 14 -3.7284959941
    # 21 -4.20338323862
    # 39 -4.87049645039
    # 56 -5.23291612556
    # 81 -5.61140135356
    # 157 -6.15723003434


def spreading_function(zmaskee,zmasker,Pmasker):
    z = zmaskee-zmasker
    c = 0
    if ((-3 <= z) and (z<-1)):
        v = (17*z)-(0.4*Pmasker)+11
        c = 1
    elif ((-1<=z) and (z<0)):
        v = ((0.4*Pmasker)+6)*z
        c = 2
    elif ((0<=z) and (z<1)):
        v = (-17)*z
        c = 3
    elif ((1<=z) and (z<8)):
        v = ((-17)*z)+(0.15*Pmasker*(z-1))
        c = 4
    if c==0:
        return -1
    if(c==1 or c==2 or c==3 or c==4):
        return 10**(v/10.0)

def tonal_nontonal_threshold(Pval,val,float_barkarray_val,mask_index,length):
    sum = 0
    for i in range(length):
        if (val[i] ==2 or val[i] ==1):
            val_spreading_fn = spreading_function(float_barkarray_val,bark_array_float[i],Pval[i])
            if(val_spreading_fn!=-1):
                l = Pval[i]+mask_index[i]+val_spreading_fn
                x = 10**(l/10.0)
                sum= sum+x
    return sum

def globalMaskingThreshold(Pval,val,mask_index,length):
    global_masker = numpy.empty(length)
    for i in range(length):
        x = tonal_nontonal_threshold(Pval,val,bark_array_float[i],mask_index,length)
        global_masker[i]=10*numpy.log10((10**(threshold_quiet_vals[i]/10))+x)
    return global_masker

def minMaskingThreshold(global_mask):
    min_masker = numpy.empty(Num_subbands)
    # print length
    # print Subband_size
    # print N_SUBBAND
    for i in range(Num_subbands):
        min_masker[i] = global_mask[mfccfilterbank_index[2*i]]
        for j in range(mfccfilterbank_index[2*i]+1,mfccfilterbank_index[(2*i)+1]+1):
                if (min_masker[i] > global_mask[j]):
                    min_masker[i] = global_mask[j]
    return min_masker

def minMaskFill(min_mask,parameter):
    fill_min_masker = numpy.ones(HalfWin+1)
    for i in range(Num_subbands):
        fill_min_masker[mfccfilterbank_index[2*i]:(mfccfilterbank_index[(2*i)+1]+1)] = (pow(10,float((min_mask[i] - parameter)/20))*watermark_strength)
    return fill_min_masker

def watermarking_block(signal,watermarkbits_expanded,Fs,Win,Step):
    Win = int(Win)
    Step = int(Step)

    # frequency_array - array of the frequencies in the Freq axis
    # threshold_quiet_vals - array of the thresholds in quiet of the values in the Freq axis
    # bark_array_float - converted from frequency to bark scale
    # bark_array - values rounded after being converted from frequency to bark scale
    # criticaldefn - the index of the frequency array that is closest to the centre frequency in each bark band 

    # Signal normalization
    signal = numpy.double(signal)
    return_signal = signal.copy()

    # TODO analyze the implcations of this
    # signal = signal / (2.0 ** 15)
    # DC = signal.mean()
    # MAX = (numpy.abs(signal)).max()
    # signal = (signal - DC) / MAX

    N              = len(signal)     # total number of samples
    curPos         = 0
    countFrames    = 0
    countUnits     = 0
    prev_watermark = numpy.zeros(Win)
    # nFFT        = Win / 2
    # print 'New Set'
    # print 'len(signal)',len(signal)
    while (1):                        # for each short-term window until the end of signal
        # take current window
        x            = signal[curPos:curPos+Win].copy()
        # hann windowing to allow smooth ends and better concatenation
        x1           = hann(x,Win)
        # FFT is performed of the time window
        X            = (fft(x1))                                    # get fft magnitude        
        #TODO separate function
        # Magnitude and argument of an FFT
        Xabs         = abs(X)
        Xangle       = numpy.angle(X)
        # normalize fft
        Xabslog      = 10*numpy.log10(numpy.square(Xabs)/(Win*Win))
        #TODO examine how needed this is
        Xabslog_norm,parameter = SPL_normalise(Xabslog,Win)
       
        # expand the PN bits with sign, expanded bits has a size of 256
        expandedbits = signexpanded(watermarkbits_expanded,countUnits,float(C[countFrames]))

        P,v              = tonal_markers_sound(Xabslog_norm[:(Win/2)+1],(Win/2)+1)
        mask_indices     = compute_masking_indices(v,len(v))
        global_mask      = globalMaskingThreshold(P,v,mask_indices,len(v))
        min_mask         = minMaskingThreshold(global_mask)
        min_mask_factors = minMaskFill(min_mask,parameter)
        # Recon_store      = numpy.empty(Step+1,dtype=complex)
        # for i in range(1,Step+1):
        #     SIN            = expandedbits[i-1]*min_mask_factors[i-1]*numpy.sin(Xangle[i])
        #     COS            = expandedbits[i-1]*min_mask_factors[i-1]*numpy.cos(Xangle[i])
        #     Recon_store[i] = complex(COS,SIN)
        # Recon_store[0]= 0

        Recon_store = numpy.empty(Win,dtype='complex')
        for i in range(1,Win/2+1):
            COS = expandedbits[i-1]*min_mask_factors[i]*numpy.cos(Xangle[i])
            SIN = expandedbits[i-1]*min_mask_factors[i]*numpy.sin(Xangle[i])
            Recon_store[i]=complex(COS,SIN)
            if(i != Win-i):
                Recon_store[Win-i]=complex(COS,-SIN)
        Recon_store[0]= 0

        value_embed      = ifft(Recon_store)
        value_embed_real = numpy.real(value_embed)
        hann_watermark   = hann(value_embed_real,Win)

        # Writing in the info from the psycho acoustic model along with the current frame and the output of the prev iteration.
        for i in range(Step):        
            return_signal[curPos+i] = prev_watermark[Step+i]+hann_watermark[i]+signal[curPos+i]
        
        # save the prev values
        for i in range(Win):
            prev_watermark[i] = hann_watermark[i];   
    
        # increment the start
        curPos       = curPos + Step 
        # print curPos
        if(curPos+Win>duration_block_point):
            return return_signal
        # U           = 4    no of frames per unit
        # B           = 10   no of units per block
        # when the number of frames reaches U,increment countFrames 
        countFrames+=1
        if(countFrames>=U):
            countFrames = 0
            countUnits+=1
        # when the number of units reaches U,encoding is done
        if(countUnits>=B):
            print 'Finished encoding one block'
            return return_signal