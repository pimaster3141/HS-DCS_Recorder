def checkOutput(data):
	index = 0;
	previousVal = data[0];
	for index in range(1, len(data)):
		previousVal = previousVal + 1;
		if previousVal > 255:
			previousVal = 1;

		if(previousVal != data[index]):
			raise Exception(index);
	return ("good");
