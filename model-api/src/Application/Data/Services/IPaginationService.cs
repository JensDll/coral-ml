using Contracts.Request;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Data.Services
{
    public interface IPaginationService
    {
        (int skip, int take) SkipTake(PaginationRequestDto paginationRequest);
    }
}
