function ATSCard({ analysis }) {

    return (

        <div className="card shadow mt-4">

            <div className="card-body">

                <h3 className="mb-4">
                    ATS Analysis
                </h3>

                <h1 className="text-success">

                    {analysis.ats_score}%

                </h1>

                <div className="progress mt-3">

                    <div

                        className="progress-bar bg-success"

                        style={{
                            width: `${analysis.ats_score}%`
                        }}

                    >

                        {analysis.ats_score}%

                    </div>

                </div>

                <hr />

                <h5>

                    Match Score

                </h5>

                <h2>

                    {analysis.match_score}%

                </h2>

            </div>

        </div>

    );

}

export default ATSCard;