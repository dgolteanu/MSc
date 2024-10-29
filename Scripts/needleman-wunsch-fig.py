# Function to add text annotations for matrix values
def plot_matrix_with_values(ax, matrix, seq1, seq2, title):
    ax.matshow(matrix, cmap='coolwarm', alpha=0.1)  # Light background color for the grid
    for (i, j), val in np.ndenumerate(matrix):
        ax.text(j, i, f'{int(val)}', ha='center', va='center')
    
    ax.set_title(title)
    ax.set_xticks(range(len(seq2) + 1))
    ax.set_yticks(range(len(seq1) + 1))
    ax.set_xticklabels(['-'] + list(seq2))
    ax.set_yticklabels(['-'] + list(seq1))

# Create subplots for the 4 steps with actual scores
fig, axs = plt.subplots(2, 2, figsize=(10, 10))

# Step 1: Initialization of the matrix
plot_matrix_with_values(axs[0, 0], matrix, seq1, seq2, 'Step 1: Initialization of Scoring Matrix')

# Step 2: Filling the matrix
plot_matrix_with_values(axs[0, 1], matrix_filled, seq1, seq2, 'Step 2: Filling Scoring Matrix')

# Step 3: Traceback with matrix scores
plot_matrix_with_values(axs[1, 0], matrix_filled, seq1, seq2, 'Step 3: Traceback Path')

# Highlight the traceback path with scores
i, j = len(seq1), len(seq2)
while i > 0 and j > 0:
    axs[1, 0].add_patch(plt.Rectangle((j, i), 1, 1, fill=False, edgecolor='yellow', lw=3))
    if seq1[i-1] == seq2[j-1]:
        i -= 1
        j -= 1
    elif matrix_filled[i][j] == matrix_filled[i-1][j] + gap_penalty:
        i -= 1
    else:
        j -= 1

# Step 4: Final Alignment
axs[1, 1].text(0.1, 0.6, f"Seq1: {alignment_a}", fontsize=12)
axs[1, 1].text(0.1, 0.4, f"Seq2: {alignment_b}", fontsize=12)
axs[1, 1].set_axis_off()
axs[1, 1].set_title('Step 4: Final Alignment')

plt.tight_layout()
plt.show()
