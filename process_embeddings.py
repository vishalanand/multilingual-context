import numpy as Math
import pylab as Plot
import matplotlib.pyplot as plt
from numpy import loadtxt

def Hbeta(D = Math.array([]), beta = 1.0):
	P = Math.exp(-D.copy() * beta);
	sumP = sum(P);
	H = Math.log(sumP) + beta * Math.sum(D * P) / sumP;
	P = P / sumP;
	return H, P;

def x2p(X = Math.array([]), tol = 1e-5, perplexity = 30.0):
	(n, d) = X.shape;
	sum_X = Math.sum(Math.square(X), 1);
	D = Math.add(Math.add(-2 * Math.dot(X, X.T), sum_X).T, sum_X);
	P = Math.zeros((n, n));
	beta = Math.ones((n, 1));
	logU = Math.log(perplexity);

	for i in range(n):
		if i % 500 == 0:
			print "Computing P-values for point ", i, " of ", n, "..."

		betamin = -Math.inf;
		betamax =  Math.inf;
		Di = D[i, Math.concatenate((Math.r_[0:i], Math.r_[i+1:n]))];
		(H, thisP) = Hbeta(Di, beta[i]);

		Hdiff = H - logU;
		tries = 0;
		while Math.abs(Hdiff) > tol and tries < 50:
			if Hdiff > 0:
				betamin = beta[i].copy();
				if betamax == Math.inf or betamax == -Math.inf:
					beta[i] = beta[i] * 2;
				else:
					beta[i] = (beta[i] + betamax) / 2;
			else:
				betamax = beta[i].copy();
				if betamin == Math.inf or betamin == -Math.inf:
					beta[i] = beta[i] / 2;
				else:
					beta[i] = (beta[i] + betamin) / 2;
			(H, thisP) = Hbeta(Di, beta[i]);
			Hdiff = H - logU;
			tries = tries + 1;

		P[i, Math.concatenate((Math.r_[0:i], Math.r_[i+1:n]))] = thisP;

	print "Mean value of sigma: ", Math.mean(Math.sqrt(1 / beta));
	return P;

def pca(X = Math.array([]), no_dims = 50):
	(n, d) = X.shape;
	X = X - Math.tile(Math.mean(X, 0), (n, 1));
	(l, M) = Math.linalg.eig(Math.dot(X.T, X));
	Y = Math.dot(X, M[:,0:no_dims]);
	return Y;

def printPlot(Y, labels, index):
	f = open("XY" + str(index) + ".csv", "w")
	#print "Word,Language,X,Y"
	f.write("Word,Language,X,Y\n")
	for i,txt in enumerate(labelsRaw):
		#print labelsRaw
		#print labelsRaw[i][3:-1] + "," + labelsRaw[i][0] + labelsRaw[i][1] + "," + str(Y[i, 0]) + str(Y[i, 1])
		f.write(labelsRaw[i][3:-1] + "," + labelsRaw[i][0] + labelsRaw[i][1] + "," + str(Y[i, 0]) + "," + str(Y[i, 1]) + "\n")

def callPlot(Y, labels, index):
	printPlot(Y, labels, index)
	return
	#'''
	Plot.scatter(Y[:,0], Y[:,1], 20, labels);
	Plot.show();
	'''
	fig, ax = plt.subplots()
	ax.scatter(Y[:,0], Y[:,1])
	'''
	for i, txt in enumerate(labelsRaw):
		abc = txt[0] + txt[1], txt[2:]
		#ax.annotate(abc, (Y[i,0]+0.01,Y[i,1]+0.01))
	plt.show()

def tsne(X = Math.array([]), no_dims = 2, initial_dims = 50, perplexity = 30.0):
	if isinstance(no_dims, float):
		print "Error: array X should have type float.";
		return -1;
	if round(no_dims) != no_dims:
		print "Error: number of dimensions should be an integer.";
		return -1;

	X = pca(X, initial_dims).real;
	(n, d) = X.shape;
	max_iter = 1000;
	initial_momentum = 0.5;
	final_momentum = 0.8;
	eta = 500;
	min_gain = 0.01;
	Y = Math.random.randn(n, no_dims);
	dY = Math.zeros((n, no_dims));
	iY = Math.zeros((n, no_dims));
	gains = Math.ones((n, no_dims));

	P = x2p(X, 1e-5, perplexity);
	P = P + Math.transpose(P);
	P = P / Math.sum(P);
	P = P * 4;									# early exaggeration
	P = Math.maximum(P, 1e-12);

	callPlot(Y, labels, 0)
	#return
	
	for iter in range(max_iter):
		sum_Y = Math.sum(Math.square(Y), 1);
		num = 1 / (1 + Math.add(Math.add(-2 * Math.dot(Y, Y.T), sum_Y).T, sum_Y));
		num[range(n), range(n)] = 0;
		Q = num / Math.sum(num);
		Q = Math.maximum(Q, 1e-12);

		PQ = P - Q;
		for i in range(n):
			dY[i,:] = Math.sum(Math.tile(PQ[:,i] * num[:,i], (no_dims, 1)).T * (Y[i,:] - Y), 0);

		if iter < 20:
			momentum = initial_momentum
		else:
			momentum = final_momentum
		gains = (gains + 0.2) * ((dY > 0) != (iY > 0)) + (gains * 0.8) * ((dY > 0) == (iY > 0));
		gains[gains < min_gain] = min_gain;
		iY = momentum * iY - eta * (gains * dY);
		Y = Y + iY;
		Y = Y - Math.tile(Math.mean(Y, 0), (n, 1));

		if (iter + 1) % 50 == 0:
			C = Math.sum(P * Math.log(P / Q));
			print "Iteration ", (iter + 1), ": error is ", C
			callPlot(Y, labels, iter+1)

		if iter == 100:
			P = P / 4;

	callPlot(Y, labels, max_iter+1);
	return Y;

def preprocess():
	fLabel = open('labels.txt', 'w')
	fX = open('X.txt', 'w')
	with open("fifty_nine.clusters.m_1000+iter_10+window_3+min_count_5+size_40.normalized") as f:
		contents = f.readlines()
		for content in contents:
			split = content.split(' ', 1)
			fLabel.write(split[0] + "\n")
			fX.write(split[1])

	fLabel.close()
	fX.close()

def loadData(fileX, fileLabel):
	X = Math.loadtxt(fileX);
	labels = []
	with open(fileLabel) as my_file:
		labels = my_file.readlines()

	return X, labels

if __name__ == "__main__":
	filecnt = "xaa"
	fileX = "X/" + filecnt
	fileLabel = "labels/" + filecnt
	X, labelsRaw = loadData(fileX, fileLabel)

	mp = {}
	mp["af"]=1; mp["ar"]=2; mp["be"]=3; mp["bg"]=4; mp["bn"]=5; mp["bs"]=6; mp["ca"]=7; mp["cs"]=8; mp["cy"]=9; mp["da"]=10; mp["de"]=11; mp["el"]=12; mp["en"]=13; mp["es"]=14; mp["et"]=15; mp["fa"]=16; mp["fi"]=17; mp["fr"]=18; mp["ga"]=19; mp["gl"]=20; mp["gm"]=21; mp["gu"]=22; mp["hi"]=23; mp["hr"]=24; mp["ht"]=25; mp["hu"]=26; mp["hy"]=27; mp["id"]=28; mp["is"]=29; mp["it"]=30; mp["iw"]=31; mp["ja"]=32; mp["jw"]=33; mp["ka"]=34; mp["kk"]=35; mp["kn"]=36; mp["ko"]=37; mp["la"]=38; mp["lt"]=39; mp["lv"]=40; mp["mg"]=41; mp["mi"]=42; mp["mk"]=43; mp["ml"]=44; mp["mn"]=45; mp["mr"]=46; mp["ms"]=47; mp["ne"]=48; mp["nl"]=49; mp["pl"]=50; mp["pt"]=51; mp["ro"]=52; mp["ru"]=53; mp["si"]=54; mp["sl"]=55; mp["so"]=56; mp["sr"]=57; mp["sv"]=58; mp["sw"]=59; mp["ta"]=60; mp["te"]=61; mp["tg"]=62; mp["tl"]=63; mp["tr"]=64; mp["uk"]=65; mp["ur"]=66; mp["uz"]=67; mp["yi"]=68; mp["zh"]=69; mp["zu"]=70

	labels = []
	for label in labelsRaw:
		labels.append(mp[label[0]+label[1]])
	Y = tsne(X, 2, 50, 20.0);
