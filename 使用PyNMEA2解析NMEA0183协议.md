#使用PyNMEA2解析NMEA0183协议

[参考网址](http://gnss.help/2018/03/01/pynmea2-readme/index.html)

[NMEA 0183](https://www.nmea.org/content/STANDARDS/NMEA_0183_Standard) 是一套定义接收机输出的标准协议，有几种不同的格式，每种都是独立的、逗点隔开文本数据。它们包含了可见的卫星、卫星状态、定位状态以及接收机速度等信息。NMEA 0183 实际上已成为所有的 GPS 接收机最通用的数据输出格式，同时它也被用于与 GPS 接收机接口的大多数的软件包里。

[pynmea2](https://pypi.python.org/pypi/pynmea2) 是一个用来处理 NMEA 0183 协议的第三方模块，本文将介绍该模块的安装与使用方法。

####简介
pynmea2 模块兼容 Python 2 和 Python 3，能够解析 GSA、GGA、GSV、RMC、VTG、GLL 等 NMEA 0183 协议定义的各类数据，功能强大。该模块目前以 MIT 协议开源并托管在 [Github](https://github.com/Knio/pynmea2) 网站上。

####安装与导入
pynmea2 包已被 PyPI 索引，你只需执行以下命令即可安装 pynmea2：
	
	pip install pynmea2

安装成功后，你就可以导入和使用 pynmea2，本文之后的示例代码都假设你已通过如下代码导入了该模块：

	import pynmea2

####从字符串解析
解析字符串中 NMEA 0183 协议的数据，可以使用 pynmea2.parse(data, check=False) 方法，其中的 check 参数指定是否对消息中的检校字段进行检查。

示例代码演示解析 GGA 数据（数据来自[维基百科](https://en.wikipedia.org/wiki/NMEA_0183)）：

	>>> line = '$GPGGA,072102.20,3905.8102148,N,11704.9412932,E,4,16,0.9,1.4010,M,-8.922,M,01,0004*42'
	>>> record = pynmea2.parse(line,True)
	>>> record
	<GGA(timestamp=datetime.time(7, 21, 2, 200000), lat='3905.8102148', lat_dir='N', lon='11704.9412932', lon_dir='E', gps_qual=4, num_sats='16', horizontal_dil='0.9', altitude=1.401, altitude_units='M', geo_sep='-8.922', geo_sep_units='M', age_gps_data='01', ref_station_id='0004')>

解析完成后，你就可以通过属性来访问记录中的各个字段了：

	>>> record.timestamp
	datetime.time(7, 21, 2, 200000)
	>>> record.latitude
	39.096836913333334
	>>> record.num_sats
	'16'

除了按照协议约定格式对数据进行解析之外，pynmea2.parse() 函数还做了一些必要的数据转换工作，将经纬度坐标转换为 Python 中的 float 类型：

	>>> print('Latitude:', record.latitude)
	Latitude: 39.096836913333334
	>>> print('Longitude:', record.longitude)
	Longitude: 117.08235488666666

此外，解析方法还为输出结果添加了额外的属性：latitude_minutes，latitude_seconds，longitude_minutes 和 longitude_seconds，它们存储了大地坐标的分、秒各部分。因此你可以方便地对坐标进行格式化输出：

	>>> print('Latitude: {:02d}°{:02d}′{:07.4f}″'.format(int(record.latitude), int(record.latitude_minutes), record.latitude_seconds))
	Latitude: 39°05′48.6129″
	>>> print('Longitude: {:02d}°{:02d}′{:07.4f}″'.format(int(record.longitude), int(record.longitude_minutes), record.longitude_seconds))
	Longitude: 117°04′56.4776″
	>>> print('Altitude: {:.3f}'.format(record.altitude))
	Altitude: 1.401

####从文件中解析
NMEA 0183 协议数据经常存储在文件中，对于这种应用场景，pynmea2 创建了 pynmea2.NMEAFile 类。你可以使用这个类对遵守 NMEA 0183 协议的文件进行处理，只需传入目标文件的路径：

	>>> nmea_file = pynmea2.NMEAFile('H:/python study/gps_line.txt')
	>>> nmea_file.readline()
	<GGA(timestamp=datetime.time(7, 20, 34), lat='3905.8186042', lat_dir='N', lon='11704.9435945', lon_dir='E', gps_qual=4, num_sats='18', horizontal_dil='0.8', altitude=1.6436, altitude_units='M', geo_sep='-8.922', geo_sep_units='M', age_gps_data='01', ref_station_id='0004')>

以上代码只是为了演示 pynmea2.NMEAFile 类最基本的使用方式。实际使用中不需要这样，该类已经实现了迭代器和上下文管理器接口。上下文管理器可以帮你打理好文件的打开与关闭，迭代器则可以让循环操作的代码更清晰易读。因此更 Pythonic 的使用姿势为：

	内容引用于NMEAFile.py

	import pynmea2

	records = []
	
	nmeafilepath = 'H:/python study/gps_line.txt'
	
	with pynmea2.NMEAFile(nmeafilepath) as nmea_file:
	    for record in nmea_file:
	        records.append(record)
	
	print('Parse nmea file path:',nmeafilepath)
	
	print('Count of records:', len(records))
	
	for i in range(len(records)):
	    print('\n%d nmea sentence:' % i)
	    print(repr(records[i]))


执行后得到如下结果：
	
	Count of records: 179

	0 nmea sentence:
	<GGA(timestamp=datetime.time(7, 20, 34), lat='3905.8186042', lat_dir='N', lon='11704.9435945', lon_dir='E', gps_qual=4, num_sats='18', horizontal_dil='0.8', altitude=1.6436, altitude_units='M', geo_sep='-8.922', geo_sep_units='M', age_gps_data='01', ref_station_id='0004')>

	未截取完整...

####从数据流解析
pynmea2 还能够直接处理 NMEA 0183 协议的数据流，你可以使用 pynmea2.NMEAStreamReader 类来解析数据流：

	>>> streamreader = pynmea2.NMEAStreamReader(input_stream)
	>>> while 1:
	...    for record in streamreader.next():
	...        print(repr(record))
	... 
	<GSV(num_messages='3', msg_num='1', num_sv_in_view='11', sv_prn_num_1='10', elevation_deg_1='63', azimuth_1='137', snr_1='17', sv_prn_num_2='07', elevation_deg_2='61', azimuth_2='098', snr_2='15', sv_prn_num_3='05', elevation_deg_3='59', azimuth_3='290', snr_3='20', sv_prn_num_4='08', elevation_deg_4='54', azimuth_4='157', snr_4='30')>
	<VTG(true_track=89.68, true_track_sym='T', mag_track=None, mag_track_sym='M', spd_over_grnd_kts=Decimal('0.00'), spd_over_grnd_kts_sym='N', spd_over_grnd_kmph=0.0, spd_over_grnd_kmph_sym='K')>
	<GLL(lat='4250.5589', lat_dir='S', lon='14718.5084', lon_dir='E', timestamp=datetime.time(9, 22, 4, 999000), status='A')>
	...

####生成 NMEA 0183 数据
上文介绍过了数据解析，你还可以使用 pynmea2 包来编码生成符合 NMEA 0183 协议的数据，只需使用合适的数据来实例化 pynmea2 中对应的类。

示例，使用下面的代码生成 GGA 数据（使用 pynmea2.GGA 类），传入的参数依次为数据源（talker）、类型（type）和字段记录（fields）：

	line = '$GPGGA,072102.20,3905.8102148,N,11704.9412932,E,4,16,0.9,1.4010,M,-8.922,M,01,0004*42'
	>>> record = pynmea2.parse(line,True)
	>>> print(record.data)
	['072102.20', '3905.8102148', 'N', '11704.9412932', 'E', '4', '16', '0.9', '1.4010', 'M', '-8.922', 'M', '01', '0004']
	>>> gen_sentence = pynmea2.GGA('GP','GGA',('072102.20', '3905.8102148', 'N', '11704.9412932', 'E', '4', '16', '0.9', '1.4010', 'M', '-8.922', 'M', '01', '0004'))
	>>> str(gen_sentence)
	'$GPGGA,072102.20,3905.8102148,N,11704.9412932,E,4,16,0.9,1.4010,M,-8.922,M,01,0004*42'

####异常处理
pynmea2 在数据解析失败时会抛出 pynmea2.nmea.ParseError 异常，在需要的时候，你可以捕获并处理它。示例：

	>>> try:
			gga_msg = pynmea2.parse('$BESTPOSA,20,1,')
		except pynmea2.nmea.ParseError:
			print('Warning: a line parseing failed!')

	
	Warning: a line parseing failed!


2/6/2020 5:26:14 PM By Caesar.