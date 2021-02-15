# Draft Review of "Lizard Cellular Automata modeling"

## 1. Question:  What is your understanding of the experiment the team is replicating?  What question does it answer?  How clear is the team's explanation?
To my understanding, your paper asks the question "can the patterns on a jeweled lizard be replicated by a cellular automata?" The paper you reference, the Manukyan paper, provides a model and data for replicating lizard skin using a CA, and you implement it. You're abstract was a bit hard to understand, and it took me a few read throughs and some out-loud paraphrasing to get the jist of it (I think). While I think the concept is really cool, I think the abstract could use some rephrasing and rewording so that your overall question is clear. I would tend to favor being explicit, even stating "We sought out to answer the question [enter question here]?". Adding a question mark really helps define what exactly you're questioning.

## 2. Methodology: Do you understand the methodology?  Does it make sense for the question?  Are there limitations you see that the team did not address?
I think I understood your methedology fairly well, at least in terms of direct implementation. Each "scale" has a probability of changing color based on the color of its neighbors, and it pretty much goes from there. I think it was wise of you to avoid implementing non-hexagonal cells, and its an assumption / modeling decision that probably doesn't have a huge impact. I don't really see any limitations for doing things the way you did.

## 3. Results: Do you understand what the results are (not yet considering their interpretation)?  If they are presented graphically, are the visualizations effective?  Do all figures have labels on the axes and captions?
I think that visualizing your cellular automata in the hexagonal grid is really cool and very straight forward. It was immediatly evident to me what was going on, and I could extrapolate from your abstract how you generated the figure (though I would add a figure caption saying that explicitly). In terms of the over figures, they were a bit hard for me to understand without any context. Generally, figures (including their captions) should be fairly self-explanitory, and I found myself trying to decipher them by scrolling back and forth between your text and your pictures. I can tell that your PMF graph with the green and black lines is probably important, but there is so much information on it that its difficult for me to undertstand what's going on. The caption adds some clarity, but it doesn't really tell me anything besides "our implementation matches the paper, and the random sample does not."

As for the brown-color extension, again, the Pygame visuals are great. However, I'm not quite sure how you got from the brown-cell visualization to the one below it (or even if that was the intent). It's not entierly obvious to me if there is a progression here or if its just a single frame with a comparison below it. Generally I think that showing 3 frames for each simulation run, one for the beginning, one for the middle, and one for the end, would really clarify how your model worked.

Bluntly, I really didn't understand what the last boxplot figure was showing. I think that further explanation of your insight could be really beneficial. If it doesn't really add anything super meaningful that can't be expressed using the figures above, I'd be tempted to just not include it.

## 4. Interpretation: Does the draft report interpret the results as an answer to the motivating question?  Does the argument hold water?
I don't really think you interpret your results from the first experiment (just the implementation). You state clearly what you did and that you produced that chart, but you never say why its important or what it means. I think that is what is missing from that section, and adding some text about why your result is important will also make the figure clearer.

Similarly, you don't really interpret the results you plot. You simply state stats and information pertaining to your graphs, but don't show why I should care or why it's important.

## 5. Replication: Are the results in the report consistent with the results from the original paper?  If so, how did the authors demonstrate that consistency.  Is it quantitative or qualitative?
In terms of replication, I think they're consistent? I think that this is answered with that graph in the first experiment section, but again, I'm not clear on what that graph shows (see comments above).

## 6. Extension: Does the report explain an extension to the original experiment clearly?  Is it a sensible extension in the sense that it has the potential to answer an interesting question that the original experiment did not answer?
I think you pose an interesting extension to the paper's experiment. However, it would be nice to see an adaptation of your original question in the format that I described above. Also, I don't see how answering that question provides some insight that the paper lacked. A few sentences explaining that would be very helpful.

## 7. Progress: Is the team roughly where they should be at this point, with a replication that is substantially complete and an extension that is clearly defined and either complete or nearly so?
Progress wise, I think you're in a really good position to have your project done by the deadline.

## 8. Presentation: Is the report written in clear, concise, correct language?  Is it consistent with the audience and goals of the report?  Does it violate any of the recommendations in my style guide?
In terms of writing, there were quite a few gramatical and word choice errors that made it very difficult to understand portions of your project. In the future, I would definitely read the paper aloud (preferebly to someone not in your group) to make sure all the sentences make sense and are phrased coherently and logically.

## 9. Mechanics: Is the report in the right directory with the right file name?  Is it formatted professionally in Markdown?  Does it include a meaningful title and the full names of the authors?  Is the bibliography in an acceptable style? 
Mechanically, everything looks good! Though, I do strongly recommend you come up with a more interesting title.
