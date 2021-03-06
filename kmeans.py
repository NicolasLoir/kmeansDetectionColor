from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import cv2
import numpy as np


def centroid_histogram(clt):
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)
    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()
    return hist


def plot_colors(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0
    # loop over the percentage of each cluster and the color of # each cluster
    for (percent, color) in zip(hist, centroids):
        print(percent)
        print(color)
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX
    return bar


def showKmeans(image, cluster):
    photoImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # reshape image
    image = photoImage.reshape((photoImage.shape[0] * photoImage.shape[1], 3))
    # def cluster
    clt = KMeans(n_clusters=cluster)
    clt.fit(image)

    # recuperer le nombre de cluster
    hist = centroid_histogram(clt)
    bar = plot_colors(hist, clt.cluster_centers_)

    # plot
    fig = plt.figure(figsize=(10, 7))
    rows = 2
    columns = 1

    fig.add_subplot(rows, columns, 1)
    plt.imshow(photoImage)
    plt.axis('off')
    plt.title("Photo")

    fig.add_subplot(rows, columns, 2)
    plt.imshow(bar)
    plt.axis('off')
    plt.title("Cluster")

    plt.show()


# read image
image = cv2.imread('./tp_images/Lenna.png')
showKmeans(image, 10)
