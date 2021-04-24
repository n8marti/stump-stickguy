import matplotlib.pyplot as plt

def draw_numberline(ymin, ymax, previous_guesses, current_limits, current_guess):
    fontsize = 24

    # Set up the figure.
    fig, ax = plt.subplots(figsize=(3, 5))
    ax.set_xlim(0, 1.5)
    ax.set_ylim(0, ymax + 1)

    # Draw lines.
    x = 1
    width = 3

    plt.vlines(x, ymin, ymax)
    plt.hlines(ymin, x - width / 10., x + width / 10.)
    plt.hlines(ymax, x - width / 10., x + width / 10.)

    # Draw previous guesses as individual ticks.
    for guess in previous_guesses:
        plt.plot(x, guess, marker='_', markersize=10, color='grey')

    # Draw current limits as a line.
    plt.plot(
        [x, x],
        current_limits,
        marker='_',
        markersize=15,
        color='red',
        linewidth=5
    )

    # Draw current guess as a single tick and label it.
    plt.plot(
        x,
        current_guess,
        marker='_',
        markersize=20,
        color='black',
    )
    plt.text(
        x - width / 3,
        current_guess - ymax / 50,
        f"{current_guess}?",
        fontsize=fontsize,
    )

    # Add ymin and ymax numbers.
    plt.text(
        x,
        ymin - ymax / 10,
        ymin,
        horizontalalignment='center',
        fontsize=fontsize
    )
    plt.text(
        x,
        ymax * 1.05,
        ymax,
        horizontalalignment='center',
        fontsize=fontsize
    )

    plt.axis('off')
    fig.savefig('data/last_numberline.png', transparent=True)
    plt.close()
    return fig
