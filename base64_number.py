rixits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/"

def base64_from_number(num):
	if num < 0:
		raise NotImplementedError("Can't represent negative numbers now")

	residual = int(num)
	result = ""
	while True:
		rixit = residual % 64
		result = rixits[rixit] + result
		residual //= 64
		if residual == 0:
			break
	return result