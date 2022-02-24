import numpy as np
import matplotlib.pyplot as plt
import warnings


def main():

    transient_array = np.genfromtxt(
        "data_0.csv",
        unpack=True,
        delimiter=",",
        skip_header=1,
        filling_values=np.nan,
        usecols=[7],
    )

    transient_array = transient_array.reshape((-1, 10))

    avg_trans_array = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        for elem in transient_array:
            avg_trans_array.append(np.nanmean(elem))

    avg_trans1 = avg_trans_array[0:11]
    avg_trans2 = avg_trans_array[11:22]
    avg_trans3 = avg_trans_array[22:33]
    avg_trans4 = avg_trans_array[33:44]

    entropy_array = np.genfromtxt(
        "data_1.csv",
        unpack=True,
        delimiter=",",
        skip_header=1,
        filling_values=np.nan,
        usecols=[7],
    )

    entropy_array = entropy_array.reshape((-1, 10))

    avg_entropy_array = []
    for elem in entropy_array:
        avg_entropy_array.append(np.mean(elem))

    avg_entropy1 = avg_entropy_array[0:11]
    avg_entropy2 = avg_entropy_array[11:22]
    avg_entropy3 = avg_entropy_array[22:33]
    avg_entropy4 = avg_entropy_array[33:44]

    t = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    fig = plt.figure(figsize=(13, 10))
    fig.suptitle(
        "Average transient lengths with differing alphabet size (k) and neighbourhood (r)"
    )
    ax1 = fig.add_subplot(221)
    ax1.set_title("k = 2, r = 1")
    ax1.set_ylim([0, 250])
    ax1.set_xlabel("Labda")
    ax1.set_ylabel("Transient length")
    ax1.plot(t, avg_trans1, "bo")

    ax2 = fig.add_subplot(222)
    ax2.set_ylim([0, 250])
    ax2.set_xlabel("Labda")
    ax2.set_ylabel("Transient length")
    ax2.set_title("k = 2, r = 2")
    ax2.plot(t, avg_trans2, "bo")

    ax3 = fig.add_subplot(223)
    ax3.set_ylim([0, 250])
    ax3.set_xlabel("Labda")
    ax3.set_ylabel("Transient length")
    ax3.set_title("k = 3, r = 1")
    ax3.plot(t, avg_trans3, "bo")

    ax4 = fig.add_subplot(224)
    ax4.set_ylim([0, 250])
    ax4.set_xlabel("Labda")
    ax4.set_ylabel("Transient length")
    ax4.set_title("k = 3, r = 2")
    ax4.plot(t, avg_trans4, "bo")

    fig.legend(["Average transient length"])

    plt.show()

    fig = plt.figure(figsize=(13, 10))
    fig.suptitle(
        "Average Shannon Entropies with differing alphabet size (k) and neighbourhood (r)"
    )

    ax1 = fig.add_subplot(221)
    ax1.set_title("k = 2, r = 1")
    ax1.set_ylim([0, 6])
    ax1.set_xlabel("Labda")
    ax1.set_ylabel("Entropy")
    ax1.plot(t, avg_entropy1, "bo")

    ax2 = fig.add_subplot(222)
    ax2.set_ylim([0, 6])
    ax2.set_xlabel("Labda")
    ax2.set_ylabel("Entropy")
    ax2.set_title("k = 2, r = 2")
    ax2.plot(t, avg_entropy2, "bo")

    ax3 = fig.add_subplot(223)
    ax3.set_ylim([0, 6])
    ax3.set_xlabel("Labda")
    ax3.set_ylabel("Entropy")
    ax3.set_title("k = 3, r = 1")
    ax3.plot(t, avg_entropy3, "bo")

    ax4 = fig.add_subplot(224)
    ax4.set_ylim([0, 6])
    ax4.set_xlabel("Labda")
    ax4.set_ylabel("Entropy")
    ax4.set_title("k = 3, r = 2")
    ax4.plot(t, avg_entropy4, "bo")

    fig.legend(["Average transient length"])

    plt.show()


if __name__ == "__main__":
    main()
