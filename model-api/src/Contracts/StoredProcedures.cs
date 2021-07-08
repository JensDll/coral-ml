using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Contracts
{
    public static class StoredProcedures
    {
        public static class Model
        {
            public const string GetAll = "spModel_GetAll";

            public const string GetById = "spModel_GetById";

            public const string Create = "spModel_Create";

            public const string Delete = "spModel_Delete";
        }
    }
}
