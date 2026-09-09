function Suggestions({ analysis }) {

    return (

        <div className="card shadow mt-4 mb-5">

            <div className="card-body">

                {/* Strengths */}
                <h3>
                    💪 Strengths
                </h3>

                <ul>

                    {analysis.strengths?.length > 0 ? (

                        analysis.strengths.map(
                            (item, index) => (
                                <li key={index}>
                                    {item}
                                </li>
                            )
                        )

                    ) : (

                        <li>
                            No strengths available.
                        </li>

                    )}

                </ul>

                <hr />

                {/* Weaknesses */}
                <h3>
                    ⚠ Weaknesses
                </h3>

                <ul>

                    {analysis.weaknesses?.length > 0 ? (

                        analysis.weaknesses.map(
                            (item, index) => (
                                <li key={index}>
                                    {item}
                                </li>
                            )
                        )

                    ) : (

                        <li>
                            No weaknesses available.
                        </li>

                    )}

                </ul>

                <hr />

                {/* Suggestions */}
                <h3>
                    🚀 Suggestions
                </h3>

                <ul>

                    {analysis.suggestions?.length > 0 ? (

                        analysis.suggestions.map(
                            (item, index) => (
                                <li key={index}>
                                    {item}
                                </li>
                            )
                        )

                    ) : (

                        <li>
                            No suggestions available.
                        </li>

                    )}

                </ul>

            </div>

        </div>

    );
}

export default Suggestions;