using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Contracts
{
    public static class ApiRoutes
    {
        private const string Base = "api";

        public static class Model
        {
            public const string GetById = Base + "/model/{id}";

            public const string SaveModel = Base + "/model";
        }
    }
}
